-- ============================================================
-- Sistema de Biblioteca - Escuela Primaria Adalberto Tejeda
-- Migracion 01: roles y personas
-- Migra ClasesBiblia/Persona.java, Usuario.java y Empleado.java
-- ============================================================

create type public.rol_usuario as enum ('administrador', 'bibliotecario', 'alumno');

-- PERFILES: datos comunes de toda persona (clase Persona).
-- auth_id es opcional: la bibliotecaria puede dar de alta la ficha
-- de un alumno sin crearle cuenta de acceso.
create table public.perfiles (
  id             uuid primary key default gen_random_uuid(),
  auth_id        uuid unique references auth.users(id) on delete set null,
  rol            public.rol_usuario not null default 'alumno',
  codigo         text not null unique,          -- REQ-USU-01 / REQ-EMP-01
  nombre         text not null check (length(trim(nombre)) > 0),
  apellido       text not null check (length(trim(apellido)) > 0),
  calle          text,
  colonia        text,
  numero         integer,
  codigo_postal  text,                          -- texto: conserva ceros a la izquierda
  telefono       text,                          -- texto: no es un valor aritmetico
  correo         text check (correo is null or correo like '%_@_%._%'),
  activo         boolean not null default true,
  creado_en      timestamptz not null default now(),
  actualizado_en timestamptz not null default now()
);

comment on table public.perfiles is
  'Datos comunes de usuarios y empleados. Migra ClasesBiblia/Persona.java';

create index perfiles_rol_idx on public.perfiles (rol) where activo;
create index perfiles_nombre_idx on public.perfiles
  using gin (to_tsvector('spanish', nombre || ' ' || apellido));

-- EMPLEADOS (REQ-EMP-01)
create table public.empleados (
  perfil_id     uuid primary key references public.perfiles(id) on delete cascade,
  tipo_empleado text not null,
  fecha_ingreso date not null default current_date
);

comment on table public.empleados is
  'Datos propios del empleado. Migra ClasesBiblia/Empleado.java';

-- USUARIOS: alumnos lectores. grado y grupo permiten la busqueda
-- "por nombre o grupo" que pide la Factibilidad Operativa.
create table public.usuarios (
  perfil_id uuid primary key references public.perfiles(id) on delete cascade,
  grado     smallint check (grado between 1 and 6),
  grupo     text check (grupo is null or length(grupo) <= 4)
);

comment on table public.usuarios is
  'Datos propios del alumno lector. Migra ClasesBiblia/Usuario.java';

create index usuarios_grado_grupo_idx on public.usuarios (grado, grupo);

create or replace function public.marcar_actualizacion()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.actualizado_en = now();
  return new;
end;
$$;

create trigger perfiles_actualizacion
  before update on public.perfiles
  for each row execute function public.marcar_actualizacion();
