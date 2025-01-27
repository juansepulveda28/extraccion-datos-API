import requests
import json
import pandas as pd
import datetime as dt
# noinspection SpellCheckingInspection


class ReadDB:

    def __init__(self):
        """This object was created to extract data from API XM"""

        self.url = "http://servapibi.xm.com.co/hourly"
        self.connection = None
        self.request = ''
        self.inventario_metricas = \
            {'Gene': [(0, 'Generacion Real', 'Sistema', 'Horaria'),
                      (1, 'Generacion Real por Recurso', 'Recurso', 'Horaria')],
             'DemaCome': [(0, 'Demanda Comercial', 'Sistema', 'Horaria'),
                          (1, 'Demanda Comercial por Agente', 'Agente', 'Horaria')],
             'AporEner': [(0, 'Aportes Energia', 'Sistema', 'Diaria'),
                          (1, 'Aportes Energia por Rio', 'Rio', 'Diaria')],
             'PrecEscaAct': [(0, 'Precio de Escasez de Activacion', 'Sistema', 'Diaria')],
             'ConsCombustibleMBTU': [(0, 'Cons. Comb. Recursos DC', 'Recurso', 'Horaria')],
             'PrecOferDesp': [(0, 'Precio de Oferta del Despacho', 'Recurso', 'Horaria')],
             'PrecBolsNaci': [(0, 'Precio de Bolsa Nacional', 'Sistema', 'Horaria')],
             'MaxPrecOferNal': [(0, 'Máximo Precio de Oferta Nacional', 'Sistema', 'Horaria')],
             'RestAliv': [(0, 'Restricciones Aliviadas', 'Sistema', 'Horaria')],
             'GeneIdea': [(0, 'Generacion Ideal', 'Sistema', 'Horaria'),
                          (1, 'Generacion Ideal', 'Recurso', 'Horaria')],
             'VoluUtilDiarEner': [(0, 'Volumen Util Diario', 'Sistema', 'Diaria'),
                                  (1, 'Volumen Util Diario por Embalse', 'Embalse', 'Diaria')],
             'RemuRealIndiv': [(0, 'RRID', 'Sistema', 'Diaria')],
             'CapEfecNeta': [(0, 'Listado de recursos térmicos CEN por mes', 'Sistema', 'Anual'),
                             (1, 'Listado Recursos Generación', 'Recurso', 'Diaria')],
             'VentContEner': [(0, 'Ventas en Contratos Energía', 'Sistema', 'Horaria'),
                              (1, 'Ventas en Contratos Energía por Agente', 'Agente', 'Horaria')],
             'CompContEner': [(0, 'Compras en Contrato Energía', 'Sistema', 'Horaria'),
                              (1, 'Compras en Contrato Energía por Agente', 'Agente', 'Horaria')],
             'CompBolsNaciEner': [(0, 'Compras en Bolsa Nacional Energía', 'Sistema', 'Horaria'),
                                  (1, 'Compras en Bolsa Nacional Energía por Agente', 'Agente', 'Horaria')],
             'PrecPromContRegu': [(0, 'Precio Promedio Contratos Regulado', 'Sistema', 'Diaria')],
             'PrecPromContNoRegu': [(0, 'Precio Promedio Contratos No Regulado', 'Sistema', 'Diaria')],
             'ConsCombAprox': [(0, 'Consumo Comb Aprox.', 'RecursoComb', 'Horaria')],
             'EmisionesCO2': [(0, 'Emisiones CO2', 'RecursoComb', 'Horaria')],
             'EmisionesCH4': [(0, 'Emisiones CH4', 'RecursoComb', 'Horaria')],
             'EmisionesN2O': [(0, 'Emisiones N2O', 'RecursoComb', 'Horaria')],
             'EmisionesCO2Eq': [(0, 'Emisiones CO2e', 'Recurso', 'Horaria')],
             'factorEmisionCO2e': [(0, 'factor emision CO2e', 'Sistema', 'Horaria')],
             'ImpoEner': [(0, 'Importaciones Energía', 'Sistema', 'Horaria')],
             'DemaOR': [(0, 'Demanda por OR', 'Agente', 'Horaria')],
             'PerdidasEner': [(0, 'Perdidas en Energía', 'Sistema', 'Horaria')],
             'DemaSIN': [(0, 'Demanda del SIN', 'Sistema', 'Diaria')],
             'DemaNoAtenProg': [(0, 'Demanda No Atendida Programada por Área', 'Area', 'Diaria'),
                                (1, 'Demanda No Atendida Programada por Subárea', 'Subarea', 'Diaria')],
             'DemaNoAtenNoProg': [(0, 'Demanda No Atendida No Programada por Área', 'Area', 'Diaria'),
                                  (1, 'Demanda No Atendida No Programada por Subárea', 'Subarea', 'Diaria')],
             'CapaUtilDiarEner': [(0, 'Capacidad Util Diario', 'Sistema', 'Diaria'),
                                  (1, 'Capacidad Util Diario por Embalse', 'Embalse', 'Diaria')],
             'AporEnerMediHist': [(0, 'Media Historica Aportes', 'Sistema', 'Diaria'),
                                  (1, 'Media Historica Aportes por Rio', 'Rio', 'Diaria')],
             'GeneSeguridad': [(0, 'Generación Seguridad', 'Recurso', 'Horaria')],
             'GeneFueraMerito': [(0, 'Generación Fuera de Merito', 'Recurso', 'Horaria')],
             'ObligEnerFirme': [(0, 'Obligaciones de Energía Firme', 'Recurso', 'Diaria')],
             'FAZNI': [(0, 'Recaudo FAZNI', 'Sistema', 'Diaria')],
             'PRONE': [(0, 'Recaudo PRONE', 'Sistema', 'Diaria')],
             'FAER': [(0, 'Recaudo FAER', 'Sistema', 'Diaria')],
             'ExpoEner': [(0, 'Exportaciones Energía', 'Sistema', 'Horaria')],
             'AporCaudal': [(0, 'Aportes Caudal por Rio', 'Rio', 'Diaria')],
             'AporCaudalMediHist': [(0, 'Aportes Media Histórica Caudal por Rio', 'Rio', 'Diaria')],
             'DemaReal': [(0, 'Demanda Real por Sistema', 'Sistema', 'Horaria'),
                          (1, 'Demanda Real por Agente', 'Agente', 'Horaria')],
             }

    def get_collections(self, coleccion):

        return self.inventario_metricas[coleccion]

    def request_data(self, coleccion, metrica, start_date, end_date):
        """ request public server data from XM by the API
        Args:
            coleccion: one of the set of variables availables at self.get_collections()
            metrica:one of this variables "DemaCome", "Gene", "GeneIdea", "PrecBolsNaci", "RestAliv"
            start_date: start date consult data
            end_date: end date consult data
        Returns: DataFrame with the raw Data
        """
        
        if coleccion not in self.inventario_metricas.keys():
            print('No existe la colección {}'.format(coleccion))
            return pd.DataFrame()
        if metrica > len(self.inventario_metricas[coleccion]):
            print('No existe la metrica')
            return pd.DataFrame()

        if self.inventario_metricas[coleccion][metrica][3] == 'Horaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = pd.concat([data, temporal_data], ignore_index=True)
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria' and coleccion == 'CapEfecNeta':
            print("Entra")
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 1:
                    end = start_date + dt.timedelta(0)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'daily')
                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = pd.concat([data, temporal_data], ignore_index=True)
                start_date = start_date + dt.timedelta(1)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 1 | (end - end_date).days != 0) | aux
        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria':
            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'daily')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = pd.concat([data, temporal_data], ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Anual':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.url = self.url.replace('hourly', 'annual')
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = pd.concat([data, temporal_data], ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux

        return data