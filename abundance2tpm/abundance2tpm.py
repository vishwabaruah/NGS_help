import pandas as pd
import glob

# Directory where all *.abundance files are stored
abundance_dir = "/home/vish/Desktop/transfer/gtf_abundance/" # change the path where *.abundance files are kept
abundance_files = glob.glob(abundance_dir + "*.abundance")

# Create an empty dataframe to hold the combined TPM data
tpm_matrix = pd.DataFrame()

# Loop through each abundance file and extract TPM values
for file in abundance_files:
    # Extract sample name from file path (assuming file name structure)
    sample_name = file.split("/")[-1].replace(".abundance", "")
    
    # Read the abundance file into a dataframe
    df = pd.read_csv(file, sep="\t")
    
    # Make sure the file has a 'Gene ID' (transcript/gene ID) and 'TPM' column
    if 'Gene ID' in df.columns and 'TPM' in df.columns:
        # Set 'Gene ID' as the index (transcript/gene identifier)
        df.set_index('Gene ID', inplace=True)
        
        # Extract only the 'TPM' column, rename it to the sample name
        df_tpm = df[['TPM']].rename(columns={'TPM': sample_name})
        
        # Merge the TPM data into the main matrix
        if tpm_matrix.empty:
            tpm_matrix = df_tpm
        else:
            tpm_matrix = tpm_matrix.join(df_tpm, how='outer')
    else:
        print(f"Error: {file} does not contain the expected 'Gene ID' and 'TPM' columns.")

# Save the final TPM matrix to a file
tpm_matrix.to_csv("TPM_matrix.csv", sep=",")
print("TPM matrix has been saved to 'TPM_matrix.csv'.")
