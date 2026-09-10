-- ============================================================
-- Migracion 03: prestamos, devoluciones y sus reglas de negocio.
-- Las reglas viven en la base para que la futura app movil las
-- herede sin reimplementarlas.
-- ============================================================

create type public.estado_prestamo as enum ('activo', 'devuelto', 'vencido');

create table public.prestamos (
  id               bigint generated always as identity primary key,

  -- restrict, no cascade: REQ-PRE-03 exige conservar el historial
  libro_id         bigint not null references public.libros(id) on delete restrict,
  usuario_id       uuid   not null references public.perfiles(id) on delete restrict,
  registrado_por   uuid references public.perfiles(id) on delete set null,

  fecha_prestamo   date not null default current_date,
  fecha_limite     date not null,
  fecha_devolucion date,
  estado           public.estado_prestamo not null default 'activo',
  creado_en        timestamptz not null default now(),

  constraint devolucion_coherente check (
    (estado = 'devuelto' and fecha_devolucion is not null)
    or (estado <> 'devuelto' and fecha_devolucion is null)
  )
);

comment on table public.prestamos is
  'Migra ClasesBiblia/Prestamo y DAOBiblia/PrestamoDao.java. El borrado en '
  'cascada del esquema Java se sustituyo por restrict: borraba el historial.';

-- REQ-PRE-01: limite de un libro por usuario, garantizado por la base.
create unique index prestamo_unico_activo_por_usuario
  on public.prestamos (usuario_id)
  where estado in ('activo', 'vencido');

create index prestamos_libro_idx on public.prestamos (libro_id);
create index prestamos_vencidos_idx on public.prestamos (fecha_limite)
  where estado in ('activo', 'vencido');

-- REQ-PRE-02: plazo de siete dias naturales.
create or replace function public.calcular_fecha_limite()
returns trigger language plpgsql set search_path = '' as $$
begin
  if new.fecha_limite is null then
    new.fecha_limite := new.fecha_prestamo + interval '7 days';
  end if;
  return new;
end;
$$;

create trigger prestamos_fecha_limite
  before insert on public.prestamos
  for each row execute function public.calcular_fecha_limite();

-- REQ-PRE-01: descuenta un ejemplar al prestar, lo reintegra al devolver.
create or replace function public.mover_inventario()
returns trigger language plpgsql set search_path = '' as $$
declare
  v_existencias integer;
  v_activo      boolean;
  v_titulo      text;
begin
  if tg_op = 'INSERT' then
    select existencias, activo, titulo
      into v_existencias, v_activo, v_titulo
      from public.libros where id = new.libro_id
      for update;

    if not v_activo then
      raise exception 'El libro "%" esta dado de baja del acervo.', v_titulo;
    end if;
    if v_existencias < 1 then
      raise exception 'No hay ejemplares disponibles de "%".', v_titulo;
    end if;

    update public.libros set existencias = existencias - 1 where id = new.libro_id;

  elsif tg_op = 'UPDATE' and new.estado = 'devuelto' and old.estado <> 'devuelto' then
    update public.libros set existencias = existencias + 1 where id = new.libro_id;
  end if;

  return new;
end;
$$;

create trigger prestamos_inventario
  after insert or update of estado on public.prestamos
  for each row execute function public.mover_inventario();

-- REQ-LIB-03: impide dar de baja un libro con prestamos activos.
create or replace function public.validar_baja_de_libro()
returns trigger language plpgsql set search_path = '' as $$
declare
  v_pendientes integer;
begin
  if old.activo and not new.activo then
    select count(*) into v_pendientes
      from public.prestamos
     where libro_id = new.id and estado in ('activo', 'vencido');

    if v_pendientes > 0 then
      raise exception
        'No se puede dar de baja "%": tiene % prestamo(s) sin devolver.',
        new.titulo, v_pendientes;
    end if;
  end if;
  return new;
end;
$$;

create trigger libros_valida_baja
  before update of activo on public.libros
  for each row execute function public.validar_baja_de_libro();

-- REQ-PRE-02: identifica automaticamente los prestamos vencidos.
create or replace function public.marcar_prestamos_vencidos()
returns integer language plpgsql security definer set search_path = '' as $$
declare
  v_afectados integer;
begin
  update public.prestamos
     set estado = 'vencido'
   where estado = 'activo' and fecha_limite < current_date;

  get diagnostics v_afectados = row_count;
  return v_afectados;
end;
$$;

-- REQ-PRE-04: bitacora de notificaciones enviadas.
create table public.notificaciones (
  id           bigint generated always as identity primary key,
  perfil_id    uuid references public.perfiles(id) on delete cascade,
  prestamo_id  bigint references public.prestamos(id) on delete set null,
  tipo         text not null check (tipo in
                 ('vencimiento_proximo', 'prestamo_vencido', 'libro_disponible')),
  destinatario text not null,
  estado       text not null default 'pendiente'
                 check (estado in ('pendiente', 'enviada', 'fallida')),
  detalle      text,
  enviada_en   timestamptz,
  creada_en    timestamptz not null default now()
);

comment on table public.notificaciones is
  'REQ-PRE-04: registro de los avisos por correo generados por el sistema.';

create index notificaciones_pendientes_idx on public.notificaciones (creada_en)
  where estado = 'pendiente';
