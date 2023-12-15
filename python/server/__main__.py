from flask import Flask, request, jsonify
import joblib
import pandas as pd
import heartpy as hp
import numpy as np

app = Flask(__name__)
scaler = joblib.load('scaler.pkl')
systole_model = joblib.load('systole_model.pkl')
diastole_model = joblib.load('diastole_model.pkl')

@app.route('/api/process-data', methods=['POST'])
def process_data():
  try:
    data = request.get_json()
    
    _, m = hp.process(np.array(data['ppg']), sample_rate = 100.0)
  
    data.pop("ppg")
    data = scaler.transform(pd.DataFrame([{**data, **m}]))

    estimated_systole = systole_model.predict(data)
    estimated_diastole = diastole_model.predict(data)

    return jsonify({'status': 'success', 'message': 'Data berhasil diproses', 'estimated_systole': estimated_systole[0], 'estimated_diastole' : estimated_diastole[0]})
  except Exception as e:
    return jsonify({'status': 'error','message': str(e)})
    
if __name__ == '__main__':
  app.run(port=3456)
  

