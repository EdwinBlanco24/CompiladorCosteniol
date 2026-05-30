import re
from tkinter import simpledialog

class Tokenizer:
    def __init__(self, rules):
        self.rules = [
            (key, re.compile(pattern))
            for key, pattern in rules.items()
        ]
        self.variables = {}

    def tokenize(self, text):
        tokens = []
        while text:
            text = text.lstrip()  # Elimina espacios en blanco al inicio
            matched = False
            for name, pattern in self.rules:
                match = pattern.match(text)
                if match:
                    token_value = match.group(0)
                    tokens.append((name, token_value))
                    text = text[match.end():]
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Error tokenizando en la línea: '{text}'")
            print(tokens)  # Imprime los tokens generados para depuración
        return tokens

    def es_declaracion_valida(self, tokens):
        if len(tokens) != 3:
            return {"consola": "", "logs": "Error Papi, Que paso?: en la declaración"}

        if tokens[0][0] == 'IDENTIFIER' and tokens[1][0] == 'TYPE' and tokens[2][0] == 'SEMICOLON':
            variable = tokens[0][1]
            tipo_variable = tokens[1][1]  # Obtener el tipo de la variable de los tokens

            # Almacenar la variable con su tipo y un valor inicial
            self.variables[variable] = {'tipo': tipo_variable, 'valor': None}
            return {"consola": "", "logs": "Excelente mi Rey! Declaración válida"}

        return {"consola": "", "logs": "Error Papi, Que paso?: en la declaración"}

    def es_asignacion_valida(self, tokens, TOKENS):

        ident = tokens[0]
        assign = tokens[1]
        semi = tokens[-1]

        if len(tokens) >= 3:
            valor = tokens[2]
        else:
            return {
                "consola": "",
                "logs": "Error Papi, Que paso?: en la asignación"
            }

        if ident[0] == 'IDENTIFIER' and assign[0] == 'ASSIGNMENT' and semi[0] == 'SEMICOLON':

            variable = ident[1]

            if variable not in self.variables:
                return {
                    "consola": "",
                    "logs": f"Error Papi, Que paso?: Variable '{variable}' no declarada."
                }


            # Operaciones matemáticas
            if len(tokens) >= 6:

                # Validar estructura exacta:
                # variable = op1 operador op2 ;

                if len(tokens) != 6:
                    return {
                        "consola": "",
                        "logs": "Error Papi, Que paso?: sintáctico en operación matemática"
                    }

                operador1 = tokens[2]
                operador = tokens[3]
                operador2 = tokens[4]

                if operador1[0] != 'IDENTIFIER':
                    return {"consola": "", "logs": "Error Papi, Que paso?: en operando 1"}

                if operador2[0] != 'IDENTIFIER':
                    return {"consola": "", "logs": "Error Papi, Que paso?: en operando 2"}

                var1 = operador1[1]
                var2 = operador2[1]

                if var1 not in self.variables:
                    return {"consola": "", "logs": f"Variable '{var1}' no la declaraste, mi Rey!"}

                if var2 not in self.variables:
                    return {"consola": "", "logs": f"Variable '{var2}' no la declaraste, mi Rey!"}

                valor1 = self.variables[var1]['valor']
                valor2 = self.variables[var2]['valor']

                try:
                    valor1 = float(valor1)
                    valor2 = float(valor2)
                except:
                    return {
                        "consola": "",
                        "logs": "Error Papi, Que paso?: operación válida sólo para números"
                    }

                if operador[0] == 'PLUS':
                    resultado_operacion = valor1 + valor2

                elif operador[0] == 'MINUS':
                    resultado_operacion = valor1 - valor2

                elif operador[0] == 'MULTIPLY':
                    resultado_operacion = valor1 * valor2

                elif operador[0] == 'DIVIDE':

                    if valor2 == 0:
                        return {
                            "consola": "",
                            "logs": "Error Papi, Que paso?: división por cero"
                        }

                    resultado_operacion = valor1 / valor2

                else:
                    return {
                        "consola": "",
                        "logs": "Error Papi, Que paso?: Operador no soportado"
                    }

                self.variables[variable]['valor'] = resultado_operacion

                return {
                    "consola": "",
                    "logs": "Excelente! Operación válida"
                }

            if variable not in self.variables:
                return {"consola": "", "logs": f"Error Papi, Que paso?: Variable '{variable}' no ha sido declarada."}

            tipo_variable = self.variables[variable]['tipo']

            # Asignación entre variables
            if valor[0] == 'IDENTIFIER':

                otra_variable = valor[1]

                if otra_variable not in self.variables:
                    return {
                        "consola": "",
                        "logs": f"Error Papi, Que paso?: Variable '{otra_variable}' no declarada."
                    }

                tipo_origen = self.variables[otra_variable]['tipo']

                if tipo_origen != tipo_variable:
                    return {
                        "consola": "",
                        "logs": "Error Papi, Que paso?: Tipos incompatibles."
                    }

                self.variables[variable]['valor'] = self.variables[otra_variable]['valor']

                return {
                    "consola": "",
                    "logs": "Excelente! Asignación válida"
                }

            # Verificar el tipo de asignación y el tipo de valor
            if valor[0] == 'METHOD_CALL':

                coincidencia = re.search(
                    r'Captura\.(Texto|Entero|Real|Logico)',
                    valor[1]
                )

                tipo_metodo = coincidencia.group(1) # type: ignore

                # Verificar si el tipo coincide
                if tipo_metodo != tipo_variable:
                    return {
                        "consola": "",
                        "logs": f"Error Papi, Que paso?: Tipo de dato no coincide para {variable}"
                    }

                # Verificar si el tipo coincide
                if tipo_metodo != tipo_variable:
                    return {
                        "consola": "",
                        "logs": f"Error Papi, Que paso?: Tipo de dato no coincide para {variable}"
                    }

                if tipo_metodo == "Entero":

                    valor_capturado = simpledialog.askinteger(
                        "Captura",
                        f"Ingrese valor para {variable}"
                    )

                    self.variables[variable]['valor'] = valor_capturado

                elif tipo_metodo == "Real":

                    valor_capturado = simpledialog.askfloat(
                        "Captura",
                        f"Ingrese valor para {variable}"
                    )

                    self.variables[variable]['valor'] = valor_capturado

                elif tipo_metodo == "Texto":

                    valor_capturado = simpledialog.askstring(
                        "Captura",
                        f"Ingrese valor para {variable}"
                    )

                    self.variables[variable]['valor'] = valor_capturado

                elif tipo_metodo == "Logico":

                    valor_capturado = simpledialog.askstring(
                        "Captura",
                        f"Ingrese Verdadero o Falso para {variable}"
                    )

                    self.variables[variable]['valor'] = valor_capturado

                return {
                    "consola": "",
                    "logs": "Excelente! Asignación válida"
                }
            
            else:
                # Validación para asignaciones directas según el tipo de la variable
                tipo_variable = self.variables[variable]['tipo']
                if tipo_variable == 'Texto' and not re.fullmatch(TOKENS['TEXT'], valor[1]):
                    return {"consola": "", "logs": f"Error Papi, Que paso?: en la línea: se esperaba una cadena de texto para {variable}"}
                elif tipo_variable == 'Entero' and not re.fullmatch(TOKENS['ENTERO'], valor[1]):
                    return {"consola": "", "logs": f"Error Papi, Que paso?: en la línea: se esperaba un entero para {variable}"}
                elif tipo_variable == 'Real' and not re.fullmatch(TOKENS['REAL'], valor[1]):
                    return {"consola": "", "logs": f"Error Papi, Que paso?: en la línea: se esperaba un real para {variable}"}
                elif tipo_variable == 'Logico' and valor[0] != 'BOOLEAN':
                    return {"consola": "", "logs": f"Error Papi, Que paso?: se esperaba un valor lógico para {variable}"}

                self.variables[variable]['valor'] = valor[1].strip('"')
                return {"consola": "", "logs": "Excelente! Asignación válida"}

        return {"consola": "", "logs": "Error Papi, Que paso?: en la asignación"}

    def analizar_declaraciones(self, texto, TOKENS):
        lineas = texto.strip().split('\n')
        resultados = []
        numero_linea = 1  # Iniciar el conteo de líneas

        for linea in lineas:
            if not linea.strip():
                numero_linea += 1
                continue # Saltar líneas vacías
            try:
                tokens = self.tokenize(linea.strip())
                if tokens:
                    resultado_linea = self.procesar_linea(tokens, TOKENS)
                    resultados.append({"linea": numero_linea, "texto": linea, "resultado": resultado_linea})
                else:
                    resultados.append({"linea": numero_linea, "texto": linea, "resultado": {"consola": "Línea vacía o no reconocida", "logs": ""}})
            except ValueError as e:
                resultados.append({"linea": numero_linea, "texto": linea, "resultado": {"consola": "", "logs": str(e)}})
                break  # Detener el análisis al encontrar el primer error
            numero_linea += 1

        return resultados

    def es_llamada_impresion_valida(self, tokens, TOKENS):
        if len(tokens) != 2:
            return {"consola": "", "logs": "Error mi Rey! en la llamada de impresión"}

        print_call, semi = tokens
        if print_call[0] != 'PRINT_CALL' or semi[0] != 'SEMICOLON':
            return {"consola": "", "logs": "Error mi Rey! en la llamada de impresión"}

        argumento_match = re.match(TOKENS['PRINT_CALL'], print_call[1])
        if argumento_match:
            argumento = argumento_match.group(1)

            # Concatenación texto + variable
            if '+' in argumento:

                partes = argumento.split('+')

                resultado_final = ""

                for parte in partes:

                    parte = parte.strip()

                    if parte.startswith('"') and parte.endswith('"'):
                        resultado_final += parte.strip('"')

                    elif parte in self.variables:

                        valor = self.variables[parte]['valor']

                        if valor is None:
                            valor = ""

                        resultado_final += str(valor)

                    else:
                        return {
                            "consola": "",
                            "logs": f"Error Papi, Que paso?: '{parte}' no reconocido."
                        }

                return {
                    "consola": resultado_final,
                    "logs": "Excelente! Llamada de impresión válida"
                }

            # Distinguir entre una cadena literal y una variable
            if argumento.startswith('"') and argumento.endswith('"'):
                # Es una cadena literal
                valor_impresion = argumento.strip('"')
            elif argumento in self.variables:
                # Es una variable, obtener solo el valor
                valor_impresion = self.variables[argumento]['valor']  # Asumiendo que cada variable es un diccionario
                
                if valor_impresion is None:
                    valor_impresion = ""  # Si la variable no tiene valor asignado, imprimir cadena vacía

                valor_impresion = str(valor_impresion) # Convertir el valor a cadena para impresión

            else:
                return {"consola": "", "logs": f"Error Papi, Que paso?: Variable '{argumento}' no ha sido declarada o asignada."}

            return {"consola": valor_impresion, "logs": "Excelente! Llamada de impresión válida"}
        else:
            return {"consola": "", "logs": "Error Papi, Que paso?: en la llamada de impresión"}
   
    def procesar_linea(self, tokens, TOKENS):
        respuesta = {"consola": "", "logs": ""}

        if tokens[0][0] == 'IDENTIFIER':
            if len(tokens) == 3 and tokens[1][0] == 'TYPE' and tokens[2][0] == 'SEMICOLON':
                # Procesamiento para declaraciones
                resultado = self.es_declaracion_valida(tokens)
            elif tokens[1][0] == 'ASSIGNMENT':
                # Procesamiento para asignaciones
                resultado = self.es_asignacion_valida(tokens, TOKENS)
            else:
                resultado = {"consola": "", "logs": "Error Papi, Que paso?: en la línea"}
        elif tokens[0][0] == 'PRINT_CALL':
            # Procesamiento para llamadas de impresión
            resultado = self.es_llamada_impresion_valida(tokens, TOKENS)
        else:
            resultado = {"consola": "", "logs": "Error Papi, Que paso?: Declaración no válida"}

        # Asegurarse de que ambos, consola y logs, son cadenas
        consola_resultado = resultado.get("consola", "")
        logs_resultado = resultado.get("logs", "")

        respuesta["consola"] += str(consola_resultado) if consola_resultado is not None else ""
        respuesta["logs"] += str(logs_resultado) if logs_resultado is not None else ""

        return respuesta

