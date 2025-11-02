#!/usr/bin/env python3
import os
import pydgraph
import model
import sys
from Utils.crear_entidades import (
    crear_agente,
    crear_empresa,
    crear_cliente,
    crear_ticket
)

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    menu_options ={
        0: "Crear datos",
        1: "Mostrar Agentes por Empresa.",
        2: "Mostrar Clientes por Empresa",
        3: "Mostrar cliente por ticket",
        4: "Mostrar Tickets por Empresa",
        5: "Mostrar Tickets por Cliente",
        6: "Mostrar Agente por Ticket",
        7: "Mostrar tickets de una empresa por tipo de problema",
        8: "Mostrar tickets de un agente por tipo de problema",
        9: "Búsqueda de Ticket por empresa por medio de palabras clave",
        10: "Búsqueda de Ticket por Agente y Empresa por medio de palabras clave",
        11: "Mostrar dirección de la empresa por medio de su ID.",
        12: "Eliminar todos los datos",
        13: "Salir", 
        14: "crea empresa",
        15: "crea agente",
        16: "crea cliente",
        17: "crea ticket",
    }
    
    for key in sorted(menu_options.keys()):
        print(f"{key} -- {menu_options[key]}")
        
# Se crean constantes para el mandejo de definiciones.
PROMPT_EMPRESA_ID = "Ingrese ID de la empresa: "
PROMPT_TICKET_ID = "Ingrese ID del Ticket: "
PROMPT_CLIENTE_NOMBRE = "Ingrese el nombre del cliente: "
PROMPT_TIPO_PROBLEMA = "Ingrese tipo de problema (en formato numérico): "
PROMPT_AGENTE_ID = "Ingrese ID del Agente: "
PROMPT_PALABRAS_CLAVE = "Ingrese palabras clave: "

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()
    
# Se crean heandlers para cada objeto del menú

def handle_option_0(client):
    model.create_data(client)

def handle_option_1(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    model.Agentes_por_empresa(client, id_empresa) # Arreglo: 'result' sin usar, eliminado

def handle_option_2(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    model.Clientes_por_empresa(client, id_empresa)

def handle_option_3(client):
    id_ticket = input(PROMPT_TICKET_ID)
    model.Cliente_por_ticket(client, id_ticket)

def handle_option_4(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    model.Tickets_por_empresa(client, id_empresa)

def handle_option_5(client):
    nombre_cliente = input(PROMPT_CLIENTE_NOMBRE)
    model.Tickets_por_cliente(client, nombre_cliente)

def handle_option_6(client):
    id_ticket = input(PROMPT_TICKET_ID)
    model.Agentes_por_ticket(client, id_ticket)

def handle_option_7(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    tipo_problema = input(PROMPT_TIPO_PROBLEMA)
    model.Tickets_por_empresa_tipo(client, id_empresa, tipo_problema)

def handle_option_8(client):
    id_agente = input(PROMPT_AGENTE_ID)
    tipo_problema = input(PROMPT_TIPO_PROBLEMA)
    model.Tickets_por_agente_tipo(client, id_agente, tipo_problema)

def handle_option_9(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    palabras_clave = input(PROMPT_PALABRAS_CLAVE)
    model.Ticket_por_empresa_palabras(client, id_empresa, palabras_clave)

def handle_option_10(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    id_agente = input(PROMPT_AGENTE_ID)
    palabras_clave = input(PROMPT_PALABRAS_CLAVE)
    model.Ticket_por_agente_empresa_palabras(client, id_empresa, id_agente, palabras_clave)

def handle_option_11(client):
    id_empresa = input(PROMPT_EMPRESA_ID)
    model.Direccion_empresa_por_id(client, id_empresa)
    
def handle_option_12(client):
    model.drop_all(client)

# Las opciones 14-17 necesitan imports, ¡los encapsulamos aquí!
def handle_option_14(client): 
    from Utils.crear_entidades import crear_empresa
    crear_empresa(client)

def handle_option_15(client):
    from Utils.crear_entidades import crear_agente
    crear_agente(client)

def handle_option_16(client):
    from Utils.crear_entidades import crear_cliente
    crear_cliente(client)

def handle_option_17(client):
    from Utils.crear_entidades import crear_ticket
    crear_ticket(client)

# --- El "Dispatcher" (Despachador) ---
# Este diccionario REEMPLAZA el 'if/elif/else'
menu_options = {
    0: handle_option_0,
    1: handle_option_1,
    2: handle_option_2,
    3: handle_option_3,
    4: handle_option_4,
    5: handle_option_5,
    6: handle_option_6,
    7: handle_option_7,
    8: handle_option_8,
    9: handle_option_9,
    10: handle_option_10,
    11: handle_option_11,
    12: handle_option_12,
    # 13 es 'salir', se maneja por separado
    14: handle_option_14,
    15: handle_option_15,
    16: handle_option_16,
    17: handle_option_17,
}

def main():
    client_stub = create_client_stub()
    client = create_client(client_stub)
    model.set_schema(client)

    while True:
        print_menu()
        try:
            option = int(input('Ingresa una opción: '))
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue
        
        # --- Lógica de Salida --
        
        if option == 13:
            print("Saliendo...")
            break
        
        # --- Dispatcher ---
        
        # 1. Buscamos la función 'handler' en el diccionario
        handler = menu_options.get(option)
        
        # 2. Si existe (no es None), la ejecutamos.
        if handler:
            handler(client)
        # 3. Si no existe (es None), es una opción inválida
        else:
            print("Opción inválida, intenta nuevamente.")
            # Arreglo: 'continue' redundante eliminado
            
    # Cierra el cliente correctamente
    close_client_stub(client_stub)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error:', e)