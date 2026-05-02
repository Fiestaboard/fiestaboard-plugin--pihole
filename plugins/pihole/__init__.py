"""Display DNS query statistics from a local Pi-hole ad blocker."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "http://{pihole_host}/admin/api.php"
USER_AGENT = "FiestaBoard Pi-hole Stats Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--pihole)"


class PiholePlugin(PluginBase):
    """Pi-hole Stats plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "pihole"

    def fetch_data(self) -> PluginResult:
        try:
            host = self.config.get("pihole_host") or "pi.hole"
            api_token = self.config.get("api_token") or ""

            params = {"summary": ""}
            if api_token:
                params["auth"] = api_token

            url = f"http://{host}/admin/api.php"
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": USER_AGENT},
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()

            dns_queries = int(data.get("dns_queries_today", 0))
            ads_blocked = int(data.get("ads_blocked_today", 0))
            ads_percentage = round(float(data.get("ads_percentage_today", 0.0)), 1)
            status = str(data.get("status", "unknown"))

            return PluginResult(
                available=True,
                data={
                    "dns_queries_today": dns_queries,
                    "ads_blocked": ads_blocked,
                    "ads_percentage": ads_percentage,
                    "status": status,
                },
            )
        except Exception as e:
            logger.exception("Error fetching Pi-hole stats")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        if not config.get("pihole_host"):
            errors.append("pihole_host is required")
        return errors

    def cleanup(self) -> None:
        pass
