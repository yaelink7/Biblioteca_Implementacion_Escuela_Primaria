-- ============================================================================
-- 10. Correcciones de la auditoria profunda del 21 de septiembre de 2026
--
-- Cuatro defectos que no se podian arreglar desde Python, en orden de
-- gravedad:
--
--   1. Escalada de privilegios. proteger_rol solo vigilaba el UPDATE de la
--      columna rol, asi que un bibliotecario podia volverse administrador
--      por dos caminos que no la tocan: dar de alta un perfil con rol
--      'administrador', o repuntar el auth_id del administrador existente
--      hacia una cuenta suya.
--   2. Cambiar el puesto de un empleado no guardaba nada: tipo_empleado vive
--      en la tabla empleados y el cliente solo escribia perfiles. El dialogo
--      decia "Se actualizaron los datos" y el dato se perdia sin error.
--   3. El inventario podia descuadrarse. mover_inventario cubria el alta y la
--      devolucion, pero no el borrado de un prestamo, ni reabrir uno
--      devuelto, ni cambiar el libro prestado.
--   4. El reloj corria en UTC. La escuela esta en Veracruz (UTC-6), asi que
--      de las 18:00 en adelante la base consideraba que ya era el dia
--      siguiente: un libro se marcaba vencido el dia que aun no vencia.
--
-- Cada bloque dice que arregla y como se comprueba.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. EL RELOJ DE LA ESCUELA
--
-- El PR #55 movio el calculo de fechas del cliente a la base para que hubiera
-- un solo reloj. Lo logro, pero ese reloj quedo en UTC. Seis sitios usaban
-- current_date; ahora todos pasan por hoy(), que devuelve la fecha en el huso
-- de la escuela. Mexico no aplica horario de verano desde 2022, asi que el
-- desfase es constante.
--
-- Comprobacion: select current_date, public.hoy(); despues de las 18:00 hora
-- de Veracruz deben diferir en un dia.
-- ----------------------------------------------------------------------------

create or replace function public.hoy()
returns date
language sql
stable
set search_path = ''
as $$
  select (now() at time zone 'America/Mexico_City')::date
$$;

comment on function public.hoy is
  'La fecha de hoy en el huso de la escuela. La base corre en UTC; Veracruz no.';

revoke execute on function public.hoy from public, anon;
grant  execute on function public.hoy to authenticated;


-- La fecha de un prestamo es la del dia en que la escuela lo registro.
alter table public.prestamos
  alter column fecha_prestamo set default public.hoy();


-- REQ-PRE-02: el plazo de siete dias deja de ser un valor por omision.
-- Antes, si el cliente enviaba una fecha_limite el disparador la respetaba,
-- de modo que la "regla" se podia saltar desde la API con un solo campo.
create or replace function public.calcular_fecha_limite()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.fecha_limite := new.fecha_prestamo + 7;
  return new;
end;
$$;

comment on function public.calcular_fecha_limite is
  'REQ-PRE-02: siete dias naturales desde el prestamo. No admite otro valor.';


-- El sello de la devolucion, con la fecha de la escuela.
create or replace function public.sellar_devolucion()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if new.estado = 'devuelto' and old.estado <> 'devuelto' then
    new.fecha_devolucion := coalesce(new.fecha_devolucion, public.hoy());
  end if;

  -- Reabrir un prestamo borra la fecha: no puede haber devuelto sin fecha
  -- ni fecha sin devolucion.
  if new.estado <> 'devuelto' then
    new.fecha_devolucion := null;
  end if;

  return new;
end;
$$;


-- El ano futuro se mide contra el ano de la escuela. El 31 de diciembre
-- despues de las 18:00, la base daba por bueno el ano siguiente.
create or replace function public.validar_ano_publicacion()
returns trigger language plpgsql set search_path = '' as $$
begin
  if new.ano_publicacion is not null then
    if new.ano_publicacion > extract(year from public.hoy()) then
      raise exception 'El ano de publicacion (%) no puede ser futuro.', new.ano_publicacion;
    end if;
    if new.ano_publicacion < 1400 then
      raise exception 'El ano de publicacion (%) no es valido.', new.ano_publicacion;
    end if;
  end if;
  return new;
end;
$$;


create or replace function public.marcar_prestamos_vencidos()
returns integer language plpgsql security definer set search_path = '' as $$
declare
  v_afectados integer;
begin
  update public.prestamos
     set estado = 'vencido'
   where estado = 'activo' and fecha_limite < public.hoy();

  get diagnostics v_afectados = row_count;
  return v_afectados;
end;
$$;


-- Las dos vistas que le dicen al bibliotecario cuanto falta o cuanto lleva
-- de retraso. Eran las que daban "vencido hace 11 dias" en una pantalla y
-- "12" en la otra; ahora ambas cuentan desde el mismo dia y el correcto.
create or replace view public.v_prestamos
with (security_invoker = on) as
select
  p.id,
  p.libro_id,
  p.usuario_id,
  p.registrado_por,
  p.fecha_prestamo,
  p.fecha_limite,
  p.fecha_devolucion,
  p.estado,
  l.titulo                                as titulo_libro,
  trim(pe.nombre || ' ' || pe.apellido)   as nombre_alumno,
  u.grado,
  u.grupo,
  case
    when p.estado = 'devuelto' then 0
    else (p.fecha_limite - public.hoy())
  end                                     as dias_restantes
from public.prestamos p
join public.libros   l  on l.id = p.libro_id
join public.perfiles pe on pe.id = p.usuario_id
left join public.usuarios u on u.perfil_id = p.usuario_id;


create or replace view public.v_deudores with (security_invoker = on) as
select p.id                            as prestamo_id,
       pe.codigo,
       pe.nombre || ' ' || pe.apellido as alumno,
       u.grado, u.grupo, pe.correo, pe.telefono,
       l.titulo                        as libro,
       p.fecha_prestamo, p.fecha_limite,
       (public.hoy() - p.fecha_limite) as dias_de_retraso
  from public.prestamos p
  join public.perfiles pe on pe.id = p.usuario_id
  left join public.usuarios u on u.perfil_id = pe.id
  join public.libros l on l.id = p.libro_id
 where p.estado in ('activo', 'vencido')
   and p.fecha_limite < public.hoy();


-- ----------------------------------------------------------------------------
-- 2. LA ESCALADA DE PRIVILEGIOS
--
-- El PR #55 cerro el hueco del cliente —una linea de Python que descartaba el
-- cambio de rol— y dejo abierto el de la base, que es el que importa: la
-- llave publishable es publica por diseno, asi que cualquiera puede llamar la
-- API sin pasar por la aplicacion.
--
-- Quedaban dos caminos, y ninguno tocaba la columna rol en un UPDATE:
--
--   a) Dar de alta un perfil con rol 'administrador'. perfiles_alta solo
--      exigia es_personal(), registrar_empleado solo rechazaba 'alumno', y
--      proteger_rol era un disparador de UPDATE.
--   b) Repuntar el auth_id del administrador existente hacia una cuenta
--      propia. Quien decide con que permisos entra alguien es el par
--      (auth_id, rol), y auth_id no estaba vigilado.
--
-- Comprobacion, con una sesion de bibliotecario:
--   insert into perfiles (codigo,nombre,apellido,rol)
--     values ('X-1','a','b','administrador');          -- debe fallar
--   update perfiles set auth_id = auth.uid() where rol = 'administrador';
--                                                       -- debe fallar
-- ----------------------------------------------------------------------------

create or replace function public.proteger_rol()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  -- Sin usuario autenticado no hay a quien escalar privilegios: es el panel
  -- de Supabase, una migracion o un proceso de servicio. Las politicas RLS
  -- ya impiden que el rol anonimo llegue hasta aqui.
  if auth.uid() is null then
    return new;
  end if;

  if tg_op = 'INSERT' then
    -- Un bibliotecario si registra personal (REQ-EMP-01), pero no puede
    -- crear a alguien por encima de el.
    if new.rol = 'administrador' and not public.es_administrador() then
      raise exception 'Solo un administrador puede registrar a otro administrador.';
    end if;
    return new;
  end if;

  if new.rol is distinct from old.rol then

    -- Nadie se cambia el suyo: sin esto, cualquiera con cuenta podria
    -- ascenderse, porque la politica de perfiles permite editar el propio.
    if old.auth_id is not null and old.auth_id = auth.uid() then
      raise exception 'No puedes cambiar tu propio perfil de acceso. Pídelo a un administrador.';
    end if;

    if not public.es_administrador() then
      raise exception 'Solo un administrador puede cambiar el perfil de acceso.';
    end if;

  end if;

  -- La cuenta a la que apunta un perfil vale tanto como el rol: quien la
  -- cambia decide con que permisos entra alguien.
  if new.auth_id is distinct from old.auth_id and not public.es_administrador() then
    raise exception 'Solo un administrador puede cambiar la cuenta de acceso de un perfil.';
  end if;

  return new;
end;
$$;

comment on function public.proteger_rol is
  'Custodia el par (rol, auth_id), que es lo que decide los permisos de alguien. Corre en alta y en modificacion.';

-- El disparador pasa a cubrir el INSERT, y el UPDATE de cualquier columna:
-- con "of rol" no se enteraba de un cambio de auth_id.
drop trigger if exists perfiles_protege_rol on public.perfiles;

create trigger perfiles_protege_rol
  before insert or update on public.perfiles
  for each row execute function public.proteger_rol();


-- La misma regla en la puerta de la RPC, para que el error salga claro en
-- lugar de llegar como violacion del disparador.
create or replace function public.registrar_empleado(
  p_codigo        text,
  p_nombre        text,
  p_apellido      text,
  p_tipo_empleado text,
  p_rol           public.rol_usuario default 'bibliotecario',
  p_correo        text     default null,
  p_telefono      text     default null,
  p_calle         text     default null,
  p_colonia       text     default null,
  p_codigo_postal text     default null,
  p_numero        integer  default null
)
returns uuid
language plpgsql
security invoker
set search_path = ''
as $$
declare
  v_id uuid;
begin
  if p_rol = 'alumno' then
    raise exception 'Un empleado no puede tener perfil de alumno.';
  end if;

  if p_rol = 'administrador'
     and auth.uid() is not null
     and not public.es_administrador() then
    raise exception 'Solo un administrador puede registrar a otro administrador.';
  end if;

  insert into public.perfiles
    (codigo, nombre, apellido, rol, correo, telefono, calle, colonia,
     codigo_postal, numero)
  values
    (p_codigo, p_nombre, p_apellido, p_rol, p_correo, p_telefono, p_calle,
     p_colonia, p_codigo_postal, p_numero)
  returning id into v_id;

  -- Si RLS rechaza este INSERT, el de perfiles se revierte con el.
  insert into public.empleados (perfil_id, tipo_empleado)
  values (v_id, p_tipo_empleado);

  return v_id;
end;
$$;


-- ----------------------------------------------------------------------------
-- 3. EL PUESTO DEL EMPLEADO QUE NO SE GUARDABA
--
-- Los datos de una persona viven en dos tablas (Corolario 3). Para el alumno
-- ya existia actualizar_alumno; para el empleado no existia nada, asi que el
-- cliente escribia perfiles y tipo_empleado se quedaba como estaba. El
-- formulario confirmaba el cambio y el puesto seguia siendo el anterior.
--
-- A diferencia de actualizar_alumno, aqui **ningun parametro tiene valor por
-- omision**: una llamada parcial no puede vaciar en silencio las columnas que
-- no se mandaron. actualizar_alumno tiene ese defecto y conviene corregirlo
-- cuando las historias #74, #75 y #76 la reescriban.
--
-- Comprobacion: cambiar el puesto de un empleado desde la pantalla, cerrar y
-- reabrir la ficha; debe conservar el valor nuevo.
-- ----------------------------------------------------------------------------

create or replace function public.actualizar_empleado(
  p_id            uuid,
  p_nombre        text,
  p_apellido      text,
  p_tipo_empleado text,
  p_rol           public.rol_usuario,
  p_correo        text,
  p_telefono      text,
  p_calle         text,
  p_colonia       text
)
returns void
language plpgsql
security invoker
set search_path = ''
as $$
begin
  -- El rol se escribe y quien decide si el cambio procede es proteger_rol.
  -- Filtrarlo aqui dejaria la regla en dos sitios y ocultaria el rechazo.
  update public.perfiles
     set nombre   = p_nombre,
         apellido = p_apellido,
         rol      = p_rol,
         correo   = p_correo,
         telefono = p_telefono,
         calle    = p_calle,
         colonia  = p_colonia
   where id = p_id
     and rol <> 'alumno';

  if not found then
    raise exception 'No se encontró el empleado indicado.';
  end if;

  -- Si este UPDATE falla, el anterior se revierte con el.
  update public.empleados
     set tipo_empleado = p_tipo_empleado
   where perfil_id = p_id;

  if not found then
    raise exception 'Ese perfil no tiene ficha de empleado. Avisa al equipo.';
  end if;
end;
$$;

comment on function public.actualizar_empleado is
  'Modificacion de empleado en una sola transaccion: perfil y ficha, o ninguno.';

revoke execute on function public.actualizar_empleado from public, anon;
grant  execute on function public.actualizar_empleado to authenticated;


-- ----------------------------------------------------------------------------
-- 4. EL INVENTARIO QUE PODIA DESCUADRARSE
--
-- mover_inventario solo miraba el INSERT y la transicion a 'devuelto', y el
-- disparador escuchaba "of estado". Tres caminos quedaban fuera:
--
--   - Borrar un prestamo abierto: el ejemplar quedaba descontado para
--     siempre. La politica prestamos_escritura autoriza el DELETE.
--   - Reabrir un prestamo devuelto: el ejemplar ya se habia reintegrado y no
--     se volvia a descontar. Repetir devolver/reabrir inflaba las
--     existencias sin techo.
--   - Cambiar el libro de un prestamo: el viejo quedaba descontado y el
--     nuevo nunca se descontaba.
--
-- Ademas la funcion era security invoker, de modo que su update sobre libros
-- estaba sujeto a RLS. Hoy funciona porque quien presta es personal; el dia
-- que un alumno pueda auto-prestarse desde la aplicacion movil, el update
-- afectaria cero filas **sin lanzar error** y el inventario dejaria de
-- moverse en silencio. Pasa a security definer.
--
-- Comprobacion, sobre un libro con existencias conocidas:
--   insert  -> baja 1      delete de ese prestamo    -> vuelve a subir 1
--   devolver -> sube 1     reabrir (estado='activo') -> vuelve a bajar 1
-- ----------------------------------------------------------------------------

create or replace function public.descontar_ejemplar(p_libro_id bigint)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_existencias integer;
  v_activo      boolean;
  v_titulo      text;
begin
  select existencias, activo, titulo
    into v_existencias, v_activo, v_titulo
    from public.libros where id = p_libro_id
    for update;

  if not v_activo then
    raise exception 'El libro "%" esta dado de baja del acervo.', v_titulo;
  end if;
  if v_existencias < 1 then
    raise exception 'No hay ejemplares disponibles de "%".', v_titulo;
  end if;

  update public.libros set existencias = existencias - 1 where id = p_libro_id;
end;
$$;

comment on function public.descontar_ejemplar is
  'Uso interno de mover_inventario. No la llames desde el cliente.';

revoke execute on function public.descontar_ejemplar from public, anon, authenticated;


create or replace function public.mover_inventario()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_abierto_antes boolean := false;
  v_abierto_ahora boolean := false;
begin
  -- Un prestamo borrado devuelve el ejemplar al estante solo si seguia fuera.
  if tg_op = 'DELETE' then
    if old.estado in ('activo', 'vencido') then
      update public.libros set existencias = existencias + 1 where id = old.libro_id;
    end if;
    return old;
  end if;

  if tg_op = 'INSERT' then
    perform public.descontar_ejemplar(new.libro_id);
    return new;
  end if;

  v_abierto_antes := old.estado in ('activo', 'vencido');
  v_abierto_ahora := new.estado in ('activo', 'vencido');

  -- Cambiar el libro prestado son dos movimientos, no uno.
  if old.libro_id is distinct from new.libro_id then
    if v_abierto_antes then
      update public.libros set existencias = existencias + 1 where id = old.libro_id;
    end if;
    if v_abierto_ahora then
      perform public.descontar_ejemplar(new.libro_id);
    end if;
    return new;
  end if;

  if v_abierto_antes and not v_abierto_ahora then
    update public.libros set existencias = existencias + 1 where id = new.libro_id;
  elsif v_abierto_ahora and not v_abierto_antes then
    -- Reabrir un prestamo vuelve a sacar el ejemplar del estante.
    perform public.descontar_ejemplar(new.libro_id);
  end if;

  return new;
end;
$$;

comment on function public.mover_inventario is
  'REQ-PRE-01: mantiene existencias al dia en alta, devolucion, reapertura, cambio de libro y borrado.';

-- Sin "of estado": el disparador tiene que enterarse tambien de un cambio de
-- libro_id y de un borrado.
drop trigger if exists prestamos_inventario on public.prestamos;

create trigger prestamos_inventario
  after insert or delete or update on public.prestamos
  for each row execute function public.mover_inventario();


-- ----------------------------------------------------------------------------
-- 5. HIGIENE: funciones de disparador sin ejecucion publica
--
-- La migracion 05 revoco las que existian entonces. sellar_devolucion y
-- proteger_rol nacieron despues y nadie repitio el patron. El riesgo es bajo
-- —Postgres rechaza invocar directamente una funcion que devuelve trigger, y
-- PostgREST no las publica—, pero proteger_rol es security definer y no hay
-- motivo para dejarla al alcance.
-- ----------------------------------------------------------------------------

revoke execute on function public.sellar_devolucion from public, anon, authenticated;
revoke execute on function public.proteger_rol      from public, anon, authenticated;
revoke execute on function public.calcular_fecha_limite from public, anon, authenticated;
revoke execute on function public.mover_inventario  from public, anon, authenticated;
revoke execute on function public.validar_ano_publicacion from public, anon, authenticated;
