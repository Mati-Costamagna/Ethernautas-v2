# HOST 4

## Identidad de red (NIC)

| Campo | Valor |
|---|---|
| Rol | Host |
| IP | 10.6.0.104 |
| MAC | AB:44:86 |
| Mascara | 255.255.0.0 |
| Gateway por defecto | 10.6.0.1 |
| MAC del gateway | AA:44:43 |

## Frame Ethernet (a transmitir)

| Campo | Valor |
|---|---|
| MAC destino | AA:44:43 |
| MAC origen | AB:44:86 |

## Paquete IP (a transmitir)

| Campo | Valor |
|---|---|
| IP origen | 10.6.0.104 |
| IP destino (DST1) | 10.4.0.102 |
| TTL | 6 |
| Payload (Hex) | F7F7 |
| Payload (Binario) | 1111011111110111 |

## Paquetes recibidos

## Frame Ethernet

| Campo | Valor |
|---|---|
| MAC destino | AB:44:86 |
| MAC origen | AA:44:43 |

## Paquete IP

| Campo | Valor |
|---|---|
| IP origen | 10.6.0.102 |
| IP destino | 10.6.0.104 |
| TTL | 4 |
| Payload (Hex) | 773C |
| Payload (Binario) | 0111011100111100 |