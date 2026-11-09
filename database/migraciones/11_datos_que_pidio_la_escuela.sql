-- ============================================================================
-- 11. Los datos que pidio la escuela en la reunion del 14 de septiembre
--
-- Cuatro historias del Sprint 1 que necesitan columnas o una tabla nueva:
--
--   1. LIB-06 (#72) La coleccion de Libros del Rincon a la que pertenece
--      cada libro.
--   2. LIB-07 (#73) La asignatura del libro.
--   3. USU-07 (#74) La CURP del alumno: opcional, con el formato oficial y
--      sin repetirse.
--   4. USU-09 (#76) El maestro de grupo, que se asigna una vez por salon y
--      lo heredan sus alumnos.
--
-- USU-08 (#75), telefono y direccion del tutor, no necesita columnas: el
-- alumno ya tiene telefono, calle, colonia, numero y codigo_postal en
-- perfiles. Que el telefono sea obligatorio y que el correo deje de pedirse
-- lo aplican el validador y el formulario.
--
-- Las reglas son las del prototipo mostaza, aprobadas por la Scrum Master
-- el 3 de noviembre de 2026. Nada de lo que ya existe cambia de valor.
-- ============================================================================


-- 1 y 2. Coleccion y asignatura del libro ------------------------------------
-- Opcionales: un libro sin clasificar guarda NULL y la restriccion lo deja
-- pasar. Las listas son las mismas de modelos/libro.py.

alter table public.libros
  add column coleccion  text,
  add column asignatura text;

alter table public.libros
  add constraint libros_coleccion_valida check (coleccion in (
    'Al sol solito', 'Pasos de luna', 'Astrolabio', 'Espejo de Urania',
    'Cometas convidados')),
  add constraint libros_asignatura_valida check (asignatura in (
    'Español', 'Matemáticas', 'Ciencias Naturales', 'Historia', 'Geografía',
    'Formación Cívica y Ética', 'Artes', 'Inglés'));

-- v_catalogo las muestra al final, para no mover las columnas que ya tenia
create or replace view public.v_catalogo with (security_invoker = on) as
select l.id, l.titulo, l.autor, l.tipo_libro, l.editorial, l.ano_publicacion,
       l.num_paginas, l.existencias, l.existencias > 0 as disponible,
       l.coleccion, l.asignatura
  from public.libros l
 where l.activo;


-- 3. CURP del alumno ---------------------------------------------------------
-- Es dato de la persona, pero solo los alumnos la llevan: va en usuarios.
-- NULL pasa el formato y no choca con la restriccion unica, asi que sigue
-- siendo opcional. El formato: 4 letras, fecha, sexo, entidad, 3 consonantes
-- internas, el diferenciador y el digito verificador.

alter table public.usuarios
  add column curp text unique;

alter table public.usuarios
  add constraint usuarios_curp_formato check (curp ~ (
    '^[A-Z][AEIOUX][A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[HM]'
    '(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)'
    '[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9][0-9]$'));

-- Las altas y los cambios de alumno reciben la CURP. Un parametro mas cambia
-- la firma de la funcion, asi que se quitan las versiones de las migraciones
-- 06 y 07: si no, quedarian dos funciones con el mismo nombre. El nuevo
-- parametro va al final y con valor por omision, para que la llamada de la
-- aplicacion anterior siga funcionando.

drop function public.registrar_alumno(
  text, text, text, smallint, text, text, text, text, text, text, integer);
drop function public.actualizar_alumno(
  uuid, text, text, smallint, text, text, text, text, text, text, integer);

create function public.registrar_alumno(
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
  p_numero        integer  default null,
  p_curp          text     default null)
returns uuid
language plpgsql
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

  insert into public.usuarios (perfil_id, grado, grupo, curp)
  values (v_id, p_grado, p_grupo, p_curp);

  return v_id;
end;
$$;

create function public.actualizar_alumno(
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
  p_numero        integer  default null,
  p_curp          text     default null)
returns void
language plpgsql
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
         grupo = p_grupo,
         curp  = p_curp
   where perfil_id = p_id;
end;
$$;

-- Los mismos permisos que les dieron las migraciones 06 y 07
revoke execute on function public.registrar_alumno  from public, anon;
revoke execute on function public.actualizar_alumno from public, anon;
grant  execute on function public.registrar_alumno  to authenticated;
grant  execute on function public.actualizar_alumno to authenticated;


-- 4. Maestro de grupo por salon ----------------------------------------------
-- Se asigna una vez por salon y lo heredan sus alumnos. Al empezar otro
-- ciclo escolar se corrige aqui, sin tocar la ficha de cada alumno.

create table public.maestros_de_grupo (
  grado          smallint    not null check (grado between 1 and 6),
  grupo          text        not null check (char_length(grupo) between 1 and 4),
  maestro        text        not null check (btrim(maestro) <> ''),
  actualizado_en timestamptz not null default now(),
  primary key (grado, grupo)
);

create trigger maestros_actualizacion
  before update on public.maestros_de_grupo
  for each row execute function public.marcar_actualizacion();

alter table public.maestros_de_grupo enable row level security;

-- Como el resto del padron: el personal lee y escribe; un alumno, nada.
create policy maestros_lectura on public.maestros_de_grupo
  for select to authenticated
  using (public.es_personal());

create policy maestros_escritura on public.maestros_de_grupo
  for all to authenticated
  using (public.es_personal())
  with check (public.es_personal());
