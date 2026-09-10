-- ============================================================
-- Migracion 05: limita quien puede invocar las funciones.
-- Supabase publica automaticamente toda funcion del esquema public
-- como endpoint REST, asi que hay que revocar lo que no debe serlo.
-- ============================================================

-- Tarea administrativa: solo la corre pg_cron o el backend.
-- Sin esto, cualquiera podia marcar prestamos como vencidos por REST.
revoke execute on function public.marcar_prestamos_vencidos() from public, anon, authenticated;
grant  execute on function public.marcar_prestamos_vencidos() to service_role;

-- Funciones de apoyo de las politicas RLS: nadie sin sesion las necesita.
-- Se conserva el permiso a authenticated porque las politicas las invocan
-- con el rol del propio usuario, y cada una devuelve unicamente
-- informacion de quien la llama, nunca de terceros.
revoke execute on function public.mi_perfil()        from public, anon;
revoke execute on function public.mi_rol()           from public, anon;
revoke execute on function public.es_personal()      from public, anon;
revoke execute on function public.es_administrador() from public, anon;

comment on function public.marcar_prestamos_vencidos() is
  'REQ-PRE-02. Se ejecuta una vez al dia desde pg_cron (historia PRE-05). '
  'No es invocable desde las aplicaciones cliente.';
