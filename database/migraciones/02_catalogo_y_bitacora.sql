-- ============================================================
-- Migracion 02: catalogo de libros y bitacora de trazabilidad
-- Migra ClasesBiblia/Publicacion.java y Libro.java
-- ============================================================

create table public.libros (
  id              bigint generated always as identity primary key,  -- REQ-LIB-01
  titulo          text not null check (length(trim(titulo)) > 0),
  autor           text not null check (length(trim(autor)) > 0),
  tipo_libro      text,
  editorial       text,
  existencias     integer not null default 0 check (existencias >= 0),
  ano_publicacion smallint,
  num_paginas     integer check (num_paginas is null or num_paginas > 0),

  -- REQ-LIB-03: baja logica, para no perder el historial de prestamos
  activo          boolean not null default true,
  motivo_baja     text,
  dado_baja_en    timestamptz,

  creado_en       timestamptz not null default now(),
  actualizado_en  timestamptz not null default now(),

  constraint baja_con_motivo check (
    activo or (motivo_baja is not null and dado_baja_en is not null)
  )
);

comment on table public.libros is
  'Catalogo del acervo. Migra ClasesBiblia/Libro.java. La columna Disponible del '
  'esquema Java se elimina: se deduce de existencias > 0 en la vista del catalogo.';

create index libros_activos_idx on public.libros (titulo) where activo;

-- REQ-BUS-01: busqueda por coincidencia parcial
create index libros_busqueda_idx on public.libros
  using gin (to_tsvector('spanish',
    coalesce(titulo,'') || ' ' || coalesce(autor,'') || ' ' || coalesce(tipo_libro,'')));

-- Corrige el defecto D-08 de las pruebas del proyecto Java: el sistema
-- aceptaba anos de publicacion futuros. Va como trigger porque un CHECK
-- no admite current_date.
create or replace function public.validar_ano_publicacion()
returns trigger language plpgsql set search_path = '' as $$
begin
  if new.ano_publicacion is not null then
    if new.ano_publicacion > extract(year from current_date) then
      raise exception 'El ano de publicacion (%) no puede ser futuro.', new.ano_publicacion;
    end if;
    if new.ano_publicacion < 1400 then
      raise exception 'El ano de publicacion (%) no es valido.', new.ano_publicacion;
    end if;
  end if;
  return new;
end;
$$;

create trigger libros_valida_ano
  before insert or update of ano_publicacion on public.libros
  for each row execute function public.validar_ano_publicacion();

create trigger libros_actualizacion
  before update on public.libros
  for each row execute function public.marcar_actualizacion();

-- REQ-LIB-02: trazabilidad de altas, cambios y bajas.
create table public.bitacora_libros (
  id            bigint generated always as identity primary key,
  libro_id      bigint not null references public.libros(id) on delete cascade,
  perfil_id     uuid references public.perfiles(id) on delete set null,
  accion        text not null check (accion in ('alta', 'modificacion', 'baja')),
  datos_antes   jsonb,
  datos_despues jsonb,
  ocurrido_en   timestamptz not null default now()
);

comment on table public.bitacora_libros is
  'REQ-LIB-02: trazabilidad de altas, cambios y bajas del catalogo.';

create index bitacora_libro_idx on public.bitacora_libros (libro_id, ocurrido_en desc);
