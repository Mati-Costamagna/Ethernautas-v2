# Tablas del router

## Tabla IP vs. MAC (ARP)

| IP | MAC Address |
|---|---|
| 10.6.0.1 | AA:44:43 |
| 10.6.0.102 | AA:43:12 |
| 10.6.0.103 | AC:44:36 |
| 10.6.0.104 | AB:44:86 |
| 10.8.0.1 | AA:43:80 |

## Tabla de ruteo

| Red destino | Next hop | Interfaz |
|---|---|---|
| 10.6.0.0/16 | Directamente conectada | LAN |
| 10.8.0.0/16 | Directamente conectada | WAN |
| 10.2.0.0/16 | 10.8.0.1 | WAN |
| 10.4.0.0/16 | 10.8.0.1 | WAN |
| 10.12.0.0/16 | 10.8.0.1 | WAN |
