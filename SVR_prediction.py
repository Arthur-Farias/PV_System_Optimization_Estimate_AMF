# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 18:41:17 2025

@author: arthur.farias
"""

import joblib
import pandas as pd


'''Antes de usar, favor ler o arquivo README'''



'''Altere path para o seu diretório'''
path = r'C:\User\...'

opt_system_size_file = rf"{path}\svr_model_OPT_SYSTEM_SIZE.pkl"
opt_LCS_file         = rf"{path}\svr_model_LCS.pkl"
opt_IRR_file         = rf"{path}\svr_model_IRR.pkl"
opt_DPT_file         = rf"{path}\svr_model_DPT.pkl"
opt_inclination_file = rf"{path}\svr_model_OPT_INCLINATION.pkl"
opt_system_size = joblib.load(opt_system_size_file)
opt_LCS         = joblib.load(opt_LCS_file)
opt_IRR         = joblib.load(opt_IRR_file)
opt_DPT         = joblib.load(opt_DPT_file)
opt_inclination = joblib.load(opt_inclination_file)



'''Modifique o exemplo abaixo apenas onde é indicado com um comment (#) para fazer as estimativas dos parâmetros ótimos no seu caso'''


estimativas = pd.DataFrame(columns = ['LAT', 
                                      'LONG', 
                                      'MEAN_ANUAL_IR_LAT_POA', 
                                      'TARIFA_TOTAL',
                                      'TARIFA_FIOB', 
                                      'DEMANDA_MENSAL', 
                                      'OPT_SYSTEM_SIZE', 
                                      'OPT_INCLINATION',
                                      'LCS',
                                      'IRR', 
                                      'DPT'])



localizacao = 'Florianópolis' # Modifique aqui o nome da sua localização

estimativas.loc[localizacao, 'LAT']  = -27.6   # Insira a Latitude desejada

estimativas.loc[localizacao, 'LONG'] = -48.6 # Insira a Longitude desejada

estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA'] = 5.51  # Insira a Irradiação média anual no plano inclinado na latitude local em (kWh/m2/dia). 
                                                              # Dica: Pode-se achar esse dado para qualquer localidade do Brasil na pg. 41 do livro "Atlas Brasileiro de Energia Solar - 2ª Edição (2017)", disponível em pdf em https://labren.ccst.inpe.br/atlas_2017.html

estimativas.loc[localizacao, 'TARIFA_TOTAL'] = 0.7 # Insira a tarifa de energia em R$/kWh. Recomendado incluir a tarifa registrada na sua conta de luz.

estimativas.loc[localizacao, 'TARIFA_FIOB']  = 0.123 # Insira a tarifa do Fio B em R$/kWh. 
                                                     # Dica: É possível encontrar o valor dessa tarifa em "Base de Dados das Tarifas das Distribuidoras de Energia Elétrica", disponível em https://portalrelatorios.aneel.gov.br/luznatarifa/basestarifas

estimativas.loc[localizacao, 'DEMANDA_MENSAL'] = 700 # Insira o gasto mensal de energia em kWh.


'''Rode o código e os resultados serão printados no console.'''


indicators_parameters = pd.DataFrame([{
                                        'DEMANDA_MENSAL': estimativas.loc[localizacao, 'DEMANDA_MENSAL'],
                                        'TARIFA_TOTAL': estimativas.loc[localizacao, 'TARIFA_TOTAL'],
                                        'TARIFA_FIOB': estimativas.loc[localizacao, 'TARIFA_FIOB'],
                                        'MEAN_ANUAL_IR_LAT_POA': estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA']                                     
                                        }])


inclination_parameters = pd.DataFrame([{ 
                                        'LAT': estimativas.loc[localizacao, 'LAT'],
                                        'LONG': estimativas.loc[localizacao, 'LONG'],
                                        'MEAN_ANUAL_IR_LAT_POA': estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA']                                        
                                        }])


estimativas.loc[localizacao, 'OPT_SYSTEM_SIZE'] = opt_system_size.predict(indicators_parameters)[0]
estimativas.loc[localizacao, 'LCS'] = opt_LCS.predict(indicators_parameters)[0]
estimativas.loc[localizacao, 'IRR'] = opt_IRR.predict(indicators_parameters)[0]
estimativas.loc[localizacao, 'DPT'] = opt_DPT.predict(indicators_parameters)[0]
estimativas.loc[localizacao, 'OPT_INCLINATION'] = opt_inclination.predict(inclination_parameters)[0]


if estimativas.loc[localizacao, 'LAT'] < -34:
    print('\n')
    print(f'Rever Latitude. A latitude {estimativas.loc[localizacao, 'LAT']}° está fora do território Brasileiro.')

elif estimativas.loc[localizacao, 'LAT'] > 6:
    print('\n')
    print(f'Rever Latitude. A latitude {estimativas.loc[localizacao, 'LAT']}° está fora do território Brasileiro.')
    
elif estimativas.loc[localizacao, 'LONG'] > -32:
    print('\n')
    print(f'Rever Longitude. A longitude {estimativas.loc[localizacao, 'LONG']}° está fora do território Brasileiro.')

elif estimativas.loc[localizacao, 'LONG'] < -74:
    print('\n')
    print(f'Rever Longitude. A longitude {estimativas.loc[localizacao, 'LONG']}° está fora do território Brasileiro.')

elif estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA'] > 7:
    print('\n')
    print(f'Rever Irradiação. A irradiação {estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA']} está muito alta. Checkar unidades. O input deve estar em kWh/m2/dia não Wh/m2/dia.')
    
elif estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA'] < 0:
    print('\n')
    print(f'Rever Irradiação. A irradiação {estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA']} está negativa.')

elif estimativas.loc[localizacao, 'TARIFA_TOTAL'] > 1.2:
    print('\n')
    print(f'Rever tarifa de energia. A tarifa de energia {estimativas.loc[localizacao, 'TARIFA_TOTAL']} R$/kWh está muito alta, limite máximo recomendado é 1.2 R$/kWh')
    
elif estimativas.loc[localizacao, 'TARIFA_TOTAL'] < 0.7:
    print('\n')
    print(f'Rever tarifa de energia. A tarifa de energia de {estimativas.loc[localizacao, 'TARIFA_TOTAL']} R$/kWh está muito baixa, limite mínimo recomendado é 0.7 R$/kWh')

elif estimativas.loc[localizacao, 'TARIFA_FIOB'] > 0.4:
    print('\n')
    print(f'Rever tarifa do fio b. A tarifa do fio b de {estimativas.loc[localizacao, 'TARIFA_FIOB']} R$/kWh está muito alta, limite máximo recomendado é 0.4 R$/kWh')

elif estimativas.loc[localizacao, 'TARIFA_FIOB'] < 0.1:
    print('\n')
    print(f'Rever tarifa do fio b. A tarifa do fio b de {estimativas.loc[localizacao, 'TARIFA_FIOB']} R$/kWh está muito baixa, limite mínimo recomendado é 0.1 R$/kWh')  

elif estimativas.loc[localizacao, 'DEMANDA_MENSAL'] > 700:
    print('\n')
    print(f'Rever Demanda mensal. A demanda mensal de {estimativas.loc[localizacao, 'DEMANDA_MENSAL']} kWh está muito alta, limite máximo recomendado é 700 kWh')

elif estimativas.loc[localizacao, 'DEMANDA_MENSAL'] < 200:
    print('\n')
    print(f'Rever Demanda mensal. A demanda mensal de {estimativas.loc[localizacao, 'DEMANDA_MENSAL']} kWh está muito baixa, limite mínimo recomendado é 200 kWh')



print('\n')
print(10*'----')
print(f'Inputs para a localização {localizacao}:')
print(f'Demanda mensal de {estimativas.loc[localizacao, 'DEMANDA_MENSAL']} kWh.')
print(f'Tarifa de energia de {estimativas.loc[localizacao, 'TARIFA_TOTAL']} R$/kWh.')
print(f'Tarifa do Fio B de {estimativas.loc[localizacao, 'TARIFA_FIOB']} R$/kWh.')
print(f'Irradiação média anual no plano inclinado na latitude de {estimativas.loc[localizacao, 'MEAN_ANUAL_IR_LAT_POA']} kWh/m2/dia.')
print(10*'----')
print('\n')
print(10*'----')
print(f'Configuração ótima do sistema PV para a localização {localizacao}:')
print(f'Tamanho ótimo do sistema: {estimativas.loc[localizacao, 'OPT_SYSTEM_SIZE']:.2f} kWp.')
print(f'Inclinação ótima dos módulos: {estimativas.loc[localizacao, 'OPT_INCLINATION']:.2f}°.')
print(10*'----')
print('\n')
print(10*'----')
print('No tamanho e inclinação ótima para esses inputs, espera-se:')
print(f'Economia de R$ {estimativas.loc[localizacao, 'LCS']:.2f}.')
print(f'Taxa interna de retorno de {estimativas.loc[localizacao, 'IRR']:.2f} %.')
anos = estimativas.loc[localizacao, 'DPT']
meses = int(round(12*(anos - int(anos)),0))
anos = int(anos)
print(f'Tempo de payback descontado de {anos} anos e {meses} meses.')
print(10*'----')






