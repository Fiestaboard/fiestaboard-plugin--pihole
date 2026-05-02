# Pi-hole Stats Setup Guide

Display DNS query statistics from a local Pi-hole ad blocker.

## Overview

The Pi-hole Stats plugin queries your Pi-hole instance's built-in API to show how many DNS queries have been made today, how many were blocked, and the blocking percentage. Works with Pi-hole v5 and v6. No external API key is required, though Pi-hole v6 uses an app password.

- API reference: https://docs.pi-hole.net/api/

### Prerequisites

Requires a running Pi-hole instance on your local network. Find your API token in Pi-hole > Settings > API/Web interface.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Pi-hole Stats**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `pihole` plugin variables:
   ```
   {{{ pihole.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `pihole.dns_queries_today` | Total DNS queries today | `12435` |
| `pihole.ads_blocked` | Number of ads/queries blocked today | `1823` |
| `pihole.ads_percentage` | Percentage of queries blocked | `14.7` |
| `pihole.status` | Pi-hole status (enabled/disabled) | `enabled` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `pihole_host` | Pi-hole Host | Hostname or IP address of your Pi-hole (e.g. 192.168.1.100 or pi.hole). | `pi.hole` |
| `api_token` | API Token | Pi-hole API token from Settings > API/Web interface. Leave blank if not required. | `` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to poll Pi-hole. | `60` |

## Troubleshooting

- **Connection refused** — verify `pihole_host` and that Pi-hole is running.
- **Empty response** — your Pi-hole may require an API token. Add it in settings.

