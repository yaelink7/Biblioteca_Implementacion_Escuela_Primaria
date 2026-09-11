-- ============================================================
-- Migracion 09: permisos operativos y proteccion del perfil de acceso
--
-- 1. El bibliotecario pasa a tener los permisos operativos del
--    administrador. En una primaria la biblioteca la atiende una sola
--    persona, y exigir un segundo perfil para dar de alta a un auxiliar
--    la dejaba bloqueada.
--
-- 2. El perfil de acceso deja de poder cambiarse desde el cliente.
--    Hasta ahora lo unico que lo impedia era una linea del codigo Python
--    que descartaba el campo, lo que dejaba el hueco abierto para quien
--    llamara la interfaz de datos directamente. Cuando los alumnos tengan
--    cuenta propia, la politica de perfiles les permite editar el suyo,
--    de modo que podrian ascenderse solos.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Permisos operativos para todo el personal
-- ------------------------------------------------------------
drop policy if exists empleados_escritura on public.empleados;

create policy empleados_escritura on public.empleados
  for all to authenticated
  using (public.es_personal())
  with check (public.es_personal());

comment on policy empleados_escritura on public.empleados is
  'REQ-EMP-01: el alta de personal la puede hacer cualquier miembro del personal. '
  'Lo que sigue reservado al administrador es cambiar el perfil de acceso.';


-- ------------------------------------------------------------
-- 2. El perfil de acceso solo lo cambia un administrador
-- ------------------------------------------------------------
create or replace function public.proteger_rol()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
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

  return new;
end;
$$;

comment on function public.proteger_rol is
  'Impide que el perfil de acceso se modifique desde el cliente sin ser administrador.';

drop trigger if exists perfiles_protege_rol on public.perfiles;

create trigger perfiles_protege_rol
  before update of rol on public.perfiles
  for each row execute function public.proteger_rol();


-- ------------------------------------------------------------
-- 3. Debe existir al menos un administrador, o nadie podra volver a
--    cambiar un perfil de acceso.
-- ------------------------------------------------------------
update public.perfiles
   set rol = 'administrador'
 where codigo = 'EMP-001'
   and not exists (select 1 from public.perfiles where rol = 'administrador');
