import os
import subprocess
import sys
import time

def run_command(command, description):
    print(f"\n{description}...")
    try:
        subprocess.run(command, shell=True, check=True, text=True)
        print(f"{description} Completed Successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during: {description}")
        print(f"Error details: {e}")
        sys.exit(1)

def main():
    print("="*50)
    print(" GAME SALES PROJECT: AUTOMATED PIPELINE")
    print("="*50)

    print("\nChecking dependencies...")
    run_command("pip install -r requirements.txt", "Installing Requirements")

    print("\nEnsure you have imported 'game_sales_schema.sql' into MySQL first!")
    time.sleep(2) 
    
    if not os.path.exists(os.path.join("data", "vgsales.csv")):
        print("\nFile not found: Please place 'vgsales.csv' in the 'data/' folder.")
        sys.exit(1)
        
    run_command("python init_database.py", "Initializing Database & Loading Data")

  
    run_command("python train_model.py", "Training Machine Learning Models")

  
    print("\nPipeline finished! Launching Dashboard...")
    print("------------------------------------------------")
    run_command("streamlit run app.py", "Launching Streamlit App")

if __name__ == "__main__":
    main()