# Diseño y Simulación de Red WAN Nacional
---

## 1. Diseño del Direccionamiento IP

### A. Direccionamiento para Enlaces WAN

* Red base WAN: `192.168.100.0/24`
* Máscara de subred para cada enlace WAN: `/29` (es decir, `255.255.255.248`). Cada subred `/29` proporciona 8 direcciones IP, de las cuales 6 son utilizables.
* IP del router de sucursal en el enlace WAN: Primera IP utilizable de su subred `/29`.
* IP del router de casa matriz en el enlace WAN (hacia la sucursal): Última IP utilizable de esa subred `/29`.

| Sucursal | Subred WAN           | Rango de la Subred      | IP WAN Router Sucursal (1ra usable) | IP WAN Router Casa Matriz (Última usable) |
| :------- | :------------------- | :---------------------- | :---------------------------------- | :---------------------------------------- |
| 1        | `192.168.100.0/29`   | `192.168.100.0` - `.7`  | `192.168.100.1`                     | `192.168.100.6`                           |
| 2        | `192.168.100.8/29`   | `192.168.100.8` - `.15` | `192.168.100.9`                     | `192.168.100.14`                          |
| 3        | `192.168.100.16/29`  | `192.168.100.16` - `.23`| `192.168.100.17`                    | `192.168.100.22`                          |
| 4        | `192.168.100.24/29`  | `192.168.100.24` - `.31`| `192.168.100.25`                    | `192.168.100.30`                          |
| 5        | `192.168.100.32/29`  | `192.168.100.32` - `.39`| `192.168.100.33`                    | `192.168.100.38`                          |
| 6        | `192.168.100.40/29`  | `192.168.100.40` - `.47`| `192.168.100.41`                    | `192.168.100.46`                          |

### B. Direccionamiento para Redes LAN Internas de Sucursales

* Red base LAN para Sucursal `n`: `10.0.n.0/24`
* Máscara de subred para cada LAN: `/24` (es decir, `255.255.255.0`).
* IP del router de sucursal en la red LAN: Primera IP utilizable de su red `/24`.
* IP del puesto de trabajo en la sucursal (para Mininet): Última IP utilizable de su red `/24`.

| Sucursal | Red LAN              | Rango de la Red         | IP LAN Router Sucursal (1ra usable) | Rango IP para Hosts (Usables)        | IP Host Ejemplo (Última usable) | Default Gateway para Hosts |
| :------- | :------------------- | :---------------------- | :---------------------------------- | :----------------------------------- | :------------------------------ | :------------------------- |
| 1        | `10.0.1.0/24`        | `10.0.1.0` - `.255`     | `10.0.1.1`                          | `10.0.1.2` - `10.0.1.254`            | `10.0.1.254`                    | `10.0.1.1`                 |
| 2        | `10.0.2.0/24`        | `10.0.2.0` - `.255`     | `10.0.2.1`                          | `10.0.2.2` - `10.0.2.254`            | `10.0.2.254`                    | `10.0.2.1`                 |
| 3        | `10.0.3.0/24`        | `10.0.3.0` - `.255`     | `10.0.3.1`                          | `10.0.3.2` - `10.0.3.254`            | `10.0.3.254`                    | `10.0.3.1`                 |
| 4        | `10.0.4.0/24`        | `10.0.4.0` - `.255`     | `10.0.4.1`                          | `10.0.4.2` - `10.0.4.254`            | `10.0.4.254`                    | `10.0.4.1`                 |
| 5        | `10.0.5.0/24`        | `10.0.5.0` - `.255`     | `10.0.5.1`                          | `10.0.5.2` - `10.0.5.254`            | `10.0.5.254`                    | `10.0.5.1`                 |
| 6        | `10.0.6.0/24`        | `10.0.6.0` - `.255`     | `10.0.6.1`                          | `10.0.6.2` - `10.0.6.254`            | `10.0.6.254`                    | `10.0.6.1`                 |

---

## 2. Esquema de Red (Conceptual para Mininet)

```mermaid
graph TD
    subgraph "Casa Matriz" 
        RC["r_central <br/>(Router Central)"]
    end

    subgraph "Sucursal 1" 
        direction TB
        RS1["r_suc1 <br/>(Router Sucursal 1)"]
        HS1["h_suc1 <br/>IP: 10.0.1.254/24 <br/>GW: 10.0.1.1"]
    end

    subgraph "Sucursal 2" 
        direction TB
        RS2["r_suc2 <br/>(Router Sucursal 2)"]
        HS2["h_suc2 <br/>IP: 10.0.2.254/24 <br/>GW: 10.0.2.1"]
    end

    %% Conexiones WAN
    RC -- "Enlace WAN 1 (192.168.100.0/29)<br/>IP r_central: .6 | IP r_suc1: .1" --> RS1
    RC -- "Enlace WAN 2 (192.168.100.8/29)<br/>IP r_central: .14 | IP r_suc2: .9" --> RS2

    %% Conexiones LAN
    RS1 -- "LAN Sucursal 1 (10.0.1.0/24)<br/>IP r_suc1: .1" --> HS1
    RS2 -- "LAN Sucursal 2 (10.0.2.0/24)<br/>IP r_suc2: .1" --> HS2
    
    %% Definiciones de Estilos (Opcional, pero mejora la apariencia)
    classDef router fill:#D6EAF8,stroke:#5DADE2,stroke-width:2px,color:#333;
    classDef host fill:#E8F8F5,stroke:#73C6B6,stroke-width:2px,color:#333;

    class RC,RS1,RS2 router;
    class HS1,HS2 host;