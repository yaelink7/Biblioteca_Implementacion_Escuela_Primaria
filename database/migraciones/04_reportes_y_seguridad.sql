-- ============================================================
-- Migracion 04: vistas de reporte y control de acceso por rol.
-- La Factibilidad Legal del Avance 1 exige limitar los datos
-- completos del alumno al perfil administrador/docente.
-- ============================================================

-- Funciones de apoyo. Son security definer para que las politicas de
-- la tabla perfiles no se llamen a si mismas de forma recursiva.
create or replace function public.mi_perfil()
returns uuid language sql stable security definer set search_path = ''
as $$ select id from public.perfiles where auth_id = auth.uid() $$;

create or replace function public.mi_rol()
returns public.rol_usuario language sql stable security definer set search_path = ''
as $$ select rol from public.perfiles where auth_id = auth.uid() $$;

create or replace function public.es_personal()
returns boolean language sql stable security definer set search_path = ''
as $$ select public.mi_rol() in ('administrador', 'bibliotecario') $$;

create or replace function public.es_administrador()
returns boolean language sql stable security definer set search_path = ''
as $$ select public.mi_rol() = 'administrador' $$;

-- ---------------- VISTAS DE REPORTE ----------------

create view public.v_catalogo with (security_invoker = on) as
select l.id, l.titulo, l.autor, l.tipo_libro, l.editorial,
       l.ano_publicacion, l.num_paginas, l.existencias,
       (l.existencias > 0) as disponible
  from public.libros l
 where l.activo;

-- REP-01: reporte de alumnos deudores, con un solo clic.
create view public.v_deudores with (security_invoker = on) as
select p.id                            as prestamo_id,
       pe.codigo,
       pe.nombre || ' ' || pe.apellido as alumno,
       u.grado, u.grupo, pe.correo, pe.telefono,
       l.titulo                        as libro,
       p.fecha_prestamo, p.fecha_limite,
       (current_date - p.fecha_limite) as dias_de_retraso
  from public.prestamos p
  join public.perfiles pe on pe.id = p.usuario_id
  left join public.usuarios u on u.perfil_id = pe.id
  join public.libros l on l.id = p.libro_id
 where p.estado in ('activo', 'vencido')
   and p.fecha_limite < current_date;

-- REP-02: libros faltantes o dados de baja del acervo.
create view public.v_libros_faltantes with (security_invoker = on) as
select l.id, l.titulo, l.autor, l.tipo_libro, l.motivo_baja, l.dado_baja_en
  from public.libros l
 where not l.activo;

-- ---------------- CONTROL DE ACCESO POR ROL ----------------

alter table public.perfiles        enable row level security;
alter table public.empleados       enable row level security;
alter table public.usuarios        enable row level security;
alter table public.libros          enable row level security;
alter table public.prestamos       enable row level security;
alter table public.bitacora_libros enable row level security;
alter table public.notificaciones  enable row level security;

-- PERFILES
create policy perfiles_lectura on public.perfiles for select to authenticated
  using (public.es_personal() or auth_id = auth.uid());
create policy perfiles_alta on public.perfiles for insert to authenticated
  with check (public.es_personal());
create policy perfiles_edicion on public.perfiles for update to authenticated
  using (public.es_personal() or auth_id = auth.uid())
  with check (public.es_personal() or auth_id = auth.uid());
create policy perfiles_baja on public.perfiles for delete to authenticated
  using (public.es_administrador());

-- EMPLEADOS: REQ-EMP-01 restringe el alta a permisos administrativos.
create policy empleados_lectura on public.empleados for select to authenticated
  using (public.es_personal());
create policy empleados_escritura on public.empleados for all to authenticated
  using (public.es_administrador()) with check (public.es_administrador());

-- USUARIOS
create policy usuarios_lectura on public.usuarios for select to authenticated
  using (public.es_personal() or perfil_id = public.mi_perfil());
create policy usuarios_escritura on public.usuarios for all to authenticated
  using (public.es_personal()) with check (public.es_personal());

-- LIBROS
create policy libros_lectura on public.libros for select to authenticated
  using (true);
create policy libros_escritura on public.libros for all to authenticated
  using (public.es_personal()) with check (public.es_personal());

-- PRESTAMOS: REQ-PRE-03, el alumno solo ve sus propios movimientos.
create policy prestamos_lectura on public.prestamos for select to authenticated
  using (public.es_personal() or usuario_id = public.mi_perfil());
create policy prestamos_escritura on public.prestamos for all to authenticated
  using (public.es_personal()) with check (public.es_personal());

-- BITACORA
create policy bitacora_lectura on public.bitacora_libros for select to authenticated
  using (public.es_personal());
create policy bitacora_alta on public.bitacora_libros for insert to authenticated
  with check (public.es_personal());

-- NOTIFICACIONES
create policy notificaciones_lectura on public.notificaciones for select to authenticated
  using (public.es_personal() or perfil_id = public.mi_perfil());
create policy notificaciones_escritura on public.notificaciones for all to authenticated
  using (public.es_personal()) with check (public.es_personal());
