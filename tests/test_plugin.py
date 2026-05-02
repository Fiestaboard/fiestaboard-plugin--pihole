"""Tests for the pihole plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.pihole import PiholePlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "pihole",
    "name": "Pi-hole Stats",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "pihole_host": {
                "type": "string",
                "title": "Pi-hole Host",
                "description": "Hostname or IP address of your Pi-hole (e.g. 192.168.1.100 or pi.hole).",
                "default": "pi.hole"
            },
            "api_token": {
                "type": "string",
                "title": "API Token",
                "description": "Pi-hole API token from Settings > API/Web interface. Leave blank if not required.",
                "default": ""
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to poll Pi-hole.",
                "default": 60,
                "minimum": 30
            }
        },
        "required": [
            "pihole_host"
        ]
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "domains_being_blocked": 185392,
    "dns_queries_today": 12435,
    "ads_blocked_today": 1823,
    "ads_percentage_today": 14.66,
    "unique_domains": 987,
    "status": "enabled"
}
""")


@pytest.fixture
def plugin():
    return PiholePlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = PiholePlugin(MANIFEST)
    p.config = json.loads("""
{
    "pihole_host": "pi.hole",
    "api_token": ""
}
""")
    return p


class TestPiholePlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "pihole"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.pihole.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "dns_queries_today" in result.data, "missing variable: dns_queries_today"
        assert "ads_blocked" in result.data, "missing variable: ads_blocked"
        assert "ads_percentage" in result.data, "missing variable: ads_percentage"
        assert "status" in result.data, "missing variable: status"

    @patch("plugins.pihole.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.pihole.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

