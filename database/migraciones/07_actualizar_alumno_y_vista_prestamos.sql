-- ============================================================
-- Migracion 07
--
-- 1. La modificacion de un alumno deja de poder quedar a medias.
--    Es el mismo defecto que la migracion 06 corrigio para las altas:
--    los datos viven en dos tablas y el cliente las actualizaba por
--    separado, asi que un fallo en la segunda dejaba los datos
--    personales nuevos junto al grado y grupo viejos.
--
-- 2. Los dias de retraso se calculan en un solo lugar.
--    Se calculaban en Python con el reloj del equipo y en la vista de
--    deudores con el de la base, que corre en UTC. Durante seis horas
--    cada dia las dos respuestas diferian en uno, de modo que la misma
--    pantalla podia decir "vencido hace 11 dias" y el reporte "12".
-- ============================================================

create or replace function public.actualizar_alumno(
  p_id            uuid,
  p_nombre        text,
  p_apellido      text,
  p_grado         smallint default null,
  p_grupo         text     default null,
  p_correo        text     default null,
  p_telefono      text     default null,
  p_calle         text     default null,
  p_colonia       text     default null,
  p_codigo_postal text     default null,
  p_numero        integer  default null
)
returns void
language plpgsql
security invoker
set search_path = ''
as $$
begin
  update public.perfiles
     set nombre        = p_nombre,
         apellido      = p_apellido,
         correo        = p_correo,
         telefono      = p_telefono,
         calle         = p_calle,
         colonia       = p_colonia,
         codigo_postal = p_codigo_postal,
         numero        = p_numero
   where id = p_id;

  if not found then
    raise exception 'No se encontró el alumno indicado.';
  end if;

  -- Si este UPDATE falla, el anterior se revierte con el.
  update public.usuarios
     set grado = p_grado,
         grupo = p_grupo
   where perfil_id = p_id;
end;
$$;

comment on function public.actualizar_alumno is
  'Modificacion de alumno en una sola transaccion: perfil y ficha, o ninguno.';

revoke execute on function public.actualizar_alumno from public, anon;
grant  execute on function public.actualizar_alumno to authenticated;


-- ------------------------------------------------------------
-- Vista unica de prestamos, con el plazo resuelto por la base.
-- dias_restantes: positivo si faltan dias, negativo si ya vencio,
-- cero si vence hoy. Un solo numero y un solo reloj.
-- ------------------------------------------------------------
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
    else (p.fecha_limite - current_date)
  end                                     as dias_restantes
from public.prestamos p
join public.libros   l  on l.id = p.libro_id
join public.perfiles pe on pe.id = p.usuario_id
left join public.usuarios u on u.perfil_id = p.usuario_id;

comment on view public.v_prestamos is
  'Prestamos con el plazo calculado por la base, para que el cliente no use su propio reloj.';
