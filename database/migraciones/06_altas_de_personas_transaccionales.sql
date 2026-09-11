-- ============================================================
-- Migracion 06: el alta de una persona deja de poder quedar a medias
--
-- Los datos de una persona viven en dos tablas: lo comun en perfiles y lo
-- propio en usuarios o empleados. El cliente hacia los dos INSERT por
-- separado, asi que cuando el segundo fallaba -por ejemplo, un bibliotecario
-- intentando dar de alta personal, que solo puede un administrador- el
-- primero ya se habia aplicado y quedaba un perfil huerfano.
--
-- Dentro de una funcion los dos INSERT forman una sola transaccion: si el
-- segundo falla, el primero se revierte solo.
--
-- Son SECURITY INVOKER a proposito: corren con los permisos de quien llama,
-- de modo que las politicas RLS siguen aplicando igual que antes.
-- ============================================================

create or replace function public.registrar_alumno(
  p_codigo        text,
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
returns uuid
language plpgsql
security invoker
set search_path = ''
as $$
declare
  v_id uuid;
begin
  insert into public.perfiles
    (codigo, nombre, apellido, rol, correo, telefono, calle, colonia,
     codigo_postal, numero)
  values
    (p_codigo, p_nombre, p_apellido, 'alumno', p_correo, p_telefono, p_calle,
     p_colonia, p_codigo_postal, p_numero)
  returning id into v_id;

  insert into public.usuarios (perfil_id, grado, grupo)
  values (v_id, p_grado, p_grupo);

  return v_id;
end;
$$;

comment on function public.registrar_alumno is
  'Alta de alumno en una sola transaccion: perfil y ficha, o ninguno.';


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

comment on function public.registrar_empleado is
  'Alta de empleado en una sola transaccion: perfil y ficha, o ninguno.';

-- Solo usuarios autenticados; las politicas RLS deciden el resto.
revoke execute on function public.registrar_alumno   from public, anon;
revoke execute on function public.registrar_empleado from public, anon;
grant  execute on function public.registrar_alumno   to authenticated;
grant  execute on function public.registrar_empleado to authenticated;

-- Limpia el perfil huerfano que dejo el defecto antes de corregirlo
delete from public.perfiles p
where p.rol <> 'alumno'
  and not exists (select 1 from public.empleados e where e.perfil_id = p.id);
