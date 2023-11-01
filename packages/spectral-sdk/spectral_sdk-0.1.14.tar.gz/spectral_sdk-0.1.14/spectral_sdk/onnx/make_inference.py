import onnxruntime as ort
import numpy as np
import json

# Define the ETH wallet address
eth_address = "0x1234567890abcdef1234567890abcdef1234567890"
# eth_address = 1.1

# def preprocess_input(eth_address):
    # Convert ETH address to a format that your models can handle
    # This is a placeholder and will likely need to be adapted
    # return np.array([list(eth_address)])
def preprocess_input(eth_address):
    # Assuming eth_address is a string, and that your model
    # expects a 1D array of float values as input.
    # This is just an example and may not match your actual use case.
    char_values = np.array([ord(char) for char in eth_address])
    float_values = char_values.astype(np.float32)  # Convert to float32
    return np.array([float_values])

def extract_floats_from_dict(d):
    return [float(value) for value in d.values()]

def preprocess_input_fake(eth_address):
    data = {'borrow_sum_borrows': 0.0, 'borrow_total_auc_eth': 0.0, 'borrow_total_borrows': 0, 'borrow_total_current_loan_eth': 0.0, 'borrow_total_interest_paid': 0.0, 'borrow_total_repays': 0, 'borrow_total_time_in_ever': 0, 'credit_mix_count': 0, 'credit_mix_count_borrow': 0, 'credit_mix_count_lending': 0, 'credit_mix_max_borrow_concentration': 0, 'credit_mix_max_lending_concentration': 0.0, 'lending_sum_redeems': 0, 'lending_total_auc_eth': 0.0, 'lending_total_deposits': 0, 'lending_total_interest_earned': 0.0, 'lending_total_time_in_ever': 0, 'liquidation_time_since_last_liquidated': 999999999, 'liquidation_total_amount_eth': 0.0, 'liquidation_total_liquidations': 0, 'misc_available_borrow_amount_eth': 0.0, 'misc_average_available_borrow_amount_eth': 0, 'misc_average_collateral_balance_eth': 0, 'misc_total_collateral_balance_eth': 0.0, 'overview_current_risk_factor': 0, 'risk_factor_avg_risk_factor': 0, 'risk_factor_counts_above_threshold': 0, 'risk_factor_max_risk_factor': 0.0, 'risk_factor_weighted_avg_risk_factor': 0}
    float_values = extract_floats_from_dict(data)
    float_values_converted = np.array([float_values]).astype(np.float32)
    return float_values_converted

def postprocess_output(raw_output):
    # Process the raw output from your models
    # This is a placeholder and will likely need to be adapted
    return raw_output.tolist()

def load_and_run_model(model_path, input_data):
    # Load the ONNX model
    sess = ort.InferenceSession(model_path)
    
    # Get the name of the input and output tensors
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    
    # Run inference
    print(f"Input name: {input_name}")
    raw_output = sess.run([output_name], {input_name: input_data})[0]
    
    return postprocess_output(raw_output)

def main():
    model_files = [f'model_{i}.onnx' for i in range(31)]  # Adjust range based on your model indices
    all_inferences = {}
    
    input_data = preprocess_input_fake(eth_address)

    
    for model_file in model_files:
        
        inference_result = load_and_run_model(model_file, input_data)
        all_inferences[model_file] = inference_result
    
    # Dump the inferences to a file
    with open('inferences.json', 'w') as f:
        json.dump(all_inferences, f, indent=4)

if __name__ == '__main__':
    model_files = [f'model_{i}.onnx' for i in range(31)]  # Adjust range based on your model indices
    
    for model_file in model_files:
        onnx_session = ort.InferenceSession(model_file)
        input_info = onnx_session.get_inputs()

        for i, input in enumerate(input_info):
            print(f'Input {i}: {input.name}')
 
    main()

