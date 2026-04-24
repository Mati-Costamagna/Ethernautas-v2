# HOST 2

## Identidad de red (NIC)

| Campo | Valor |
|---|---|
| Rol | Host |
| IP | 10.6.0.102 |
| MAC | AA:43:12 |
| Mascara | 255.255.0.0 |
| Gateway por defecto | 10.6.0.1 |
| MAC del gateway | AA:44:43 |

## Frame Ethernet (a transmitir)

| Campo | Valor |
|---|---|
| MAC destino | AA:44:43 |
| MAC origen | AA:43:12 |

## Paquete IP (a transmitir)

| Campo | Valor |
|---|---|
| IP origen | 10.6.0.102 |
| IP destino (DST1) | 10.6.0.104 |
| TTL | 6 |
| Payload (Hex) | B544 |
| Payload (Binario) | 1011010101000100 |

## Paquetes recibidos

## Frame Ethernet

| Campo | Valor |
|---|---|
| MAC destino | AA:43:12 |
| MAC origen | AA:44:43 |

## Paquete IP

| Campo | Valor |
|---|---|
| IP origen | 10.9.0.101 |
| IP destino | 10.6.0.102 |
| TTL | 3 |
| Payload (Hex) | EDB2 |
| Payload (Binario) | 1110110110110010 |
