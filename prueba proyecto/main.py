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

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()

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

        if option == 0: # Funciona
            model.create_data(client)
        elif option == 1:
            id_empresa = input("Ingrese ID de la empresa: ")
            result = model.Agentes_por_empresa(client, id_empresa)

        elif option == 2: # Funciona
            id_empresa = input("Ingrese ID de la empresa: ")
            result = model.Clientes_por_empresa(client, id_empresa)

        elif option == 3: # Funciona
            id_ticket = input("Ingrese ID del Ticket: ")
            result = model.Cliente_por_ticket(client, id_ticket)

        elif option == 4: # Funciona
            id_empresa = input("Ingrese ID de la empresa: ")
            result = model.Tickets_por_empresa(client, id_empresa)

        elif option == 5: # Funciona
            nombre_cliente = input("Ingrese el nombre del cliente: ")
            result = model.Tickets_por_cliente(client, nombre_cliente)

        elif option == 6: # Funciona
            id_ticket = input("Ingrese ID del ticket: ")
            result = model.Agentes_por_ticket(client, id_ticket)

        elif option == 7: # Funciona
            id_empresa = input("Ingrese ID de la empresa: ")
            tipo_problema = input("Ingrese tipo de problema (en formato numérico): ")
            result = model.Tickets_por_empresa_tipo(client, id_empresa, tipo_problema)

        elif option == 8: # 
            id_agente = input("Ingrese ID del Agente: ")
            tipo_problema = input("Ingrese tipo de problema (en formato numérico): ")
            result = model.Tickets_por_agente_tipo(client, id_agente, tipo_problema)

        elif option == 9: # Funciona
            id_empresa = input("Ingrese ID de la empresa: ")
            palabras_clave = input("Ingrese palabras clave: ")
            result = model.Ticket_por_empresa_palabras(client, id_empresa, palabras_clave)

        elif option == 10: # Funciona
            id_empresa = input("Ingrese ID de la empresa: ")
            id_agente = input("Ingrese ID del agente: ")
            palabras_clave = input("Ingrese palabras clave: ")
            result = model.Ticket_por_agente_empresa_palabras(client, id_empresa, id_agente, palabras_clave)

        elif option == 11:
            id_empresa = input("Ingrese ID de la empresa: ")
            result = model.Direccion_empresa_por_id(client, id_empresa)
            
        elif option == 12:
            model.drop_all(client)
        elif option == 13:
            print("Saliendo...")
            break
        elif option == 14: 
            from Utils.crear_entidades import crear_empresa
            crear_empresa(client)
        elif option == 15:
            from Utils.crear_entidades import crear_agente
            crear_agente(client)
        elif option == 16:
            from Utils.crear_entidades import crear_cliente
            crear_cliente(client)
        elif option == 17:
            from Utils.crear_entidades import crear_ticket
            crear_ticket(client)

        else:
            print("Opción inválida, intenta nuevamente.")
            continue

    # Cierra el cliente correctamente
    close_client_stub(client_stub)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error:', e)