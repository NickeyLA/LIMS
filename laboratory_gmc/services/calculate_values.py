from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 10


class CalculateValues:

    @staticmethod
    def calculate_values(values_obj):
        result: dict[str, Decimal | None] = {
            "v2o5": None,
            "h2so4": None,
            "mgso4": None,
            "susp": None,
            "dry_residue": None,
        }

        try:
            # --- V2O5 / H2SO4 ---
            if (
                values_obj.v_al_ml is not None and
                values_obj.v_titr_ml is not None and
                values_obj.titrant_value and
                values_obj.titrant_value.t_titr is not None
            ):
                t_titr = values_obj.titrant_value.t_titr
                v_titr = values_obj.v_titr_ml
                v_al = values_obj.v_al_ml

                if values_obj.indicator and values_obj.indicator.indicator_name == "V2O5":
                    result["v2o5"] = (t_titr * v_titr * Decimal(1000)) / v_al
                elif values_obj.indicator and values_obj.indicator.indicator_name == "H2SO4":
                    result["h2so4"] = (t_titr * v_titr * Decimal(1000)) / v_al

            # --- MgSO4 ---
            if (
                values_obj.p_gl is not None and
                values_obj.t_oc is not None and
                values_obj.ph_density is not None
            ):
                exp_value = (Decimal("0.019") * values_obj.t_oc - Decimal("1.82") * values_obj.ph_density + Decimal("4.09")).exp()
                if Decimal("0.1") < values_obj.p_gl < Decimal("1070"):
                    result["mgso4"] = (
                        Decimal("2.057") * values_obj.p_gl + Decimal("0.718") * values_obj.t_oc
                        - Decimal("2070") - Decimal("1.353") * exp_value
                    )
                elif values_obj.p_gl >= Decimal("1070"):
                    result["mgso4"] = (
                        Decimal("2.427") * values_obj.p_gl + Decimal("0.977") * values_obj.t_oc
                        - Decimal("2070") - Decimal("2471") - Decimal("1.353") * exp_value
                    )

            # --- Susp ---
            if (
                values_obj.m_f_os is not None and
                values_obj.m_f_g is not None and
                values_obj.v_ppa_ml is not None
            ):
                result["susp"] = ((values_obj.m_f_os - values_obj.m_f_g) * Decimal(1000)) / values_obj.v_ppa_ml

            # --- Dry residue ---
            if getattr(values_obj, "dry_residue", None):
                if values_obj.v_titr_ml is not None:
                    result["dry_residue"] = (
                            Decimal("1.8") * values_obj.v_titr_ml + Decimal("6.66")
                    ).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            else:
                result["dry_residue"] = None



        except Exception as e:
            print(f"Ошибка при расчётах: {e}")

        return result
