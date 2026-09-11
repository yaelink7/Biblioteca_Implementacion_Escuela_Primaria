-- ============================================================
-- Migracion 08: la fecha de devolucion la pone la base
--
-- El cliente la enviaba con date.today(), es decir con el reloj del equipo,
-- mientras el resto de las fechas del prestamo las pone Postgres en UTC.
-- Un libro devuelto a las 7 de la noche quedaba registrado con la fecha del
-- dia anterior respecto de su propia fecha de prestamo.
--
-- Ahora basta con marcar el prestamo como devuelto: la fecha se pone sola,
-- con el mismo reloj que calculo el plazo.
-- ============================================================

create or replace function public.sellar_devolucion()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if new.estado = 'devuelto' and old.estado <> 'devuelto' then
    new.fecha_devolucion := coalesce(new.fecha_devolucion, current_date);
  end if;

  -- Reabrir un prestamo borra la fecha: no puede haber devuelto sin fecha
  -- ni fecha sin devolucion.
  if new.estado <> 'devuelto' then
    new.fecha_devolucion := null;
  end if;

  return new;
end;
$$;

create trigger prestamos_sella_devolucion
  before update of estado on public.prestamos
  for each row execute function public.sellar_devolucion();

comment on function public.sellar_devolucion is
  'Pone la fecha de devolucion con el reloj de la base, no con el del cliente.';
