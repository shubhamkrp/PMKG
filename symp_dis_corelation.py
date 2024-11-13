# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # Define the directory containing the CSV files
# directory = '/mnt/0C6C8FC06C8FA2D6/sparse_results_cui_new'

# # Lists to store aggregated data
# positive_counts = []
# negative_counts = []
# symptom_names = []

# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         filepath = os.path.join(directory, filename)
        
#         # Load CSV file into a DataFrame
#         df = pd.read_csv(filepath)
        
#         # Assuming the CSV has columns: 'symptom_name', 'positive_count', 'negative_count'
#         for _, row in df.iterrows():
#             positive_counts.append(row['positive_count'])
#             negative_counts.append(row['negative_count'])
#             symptom_names.append(row['symptom'])
# print(len(symptom_names))
# # Create the scatter plot
# plt.figure(figsize=(10, 6))
# plt.scatter(positive_counts, negative_counts, alpha=0.5)
# plt.xlabel("Positive Count")
# plt.ylabel("Negative Count")
# plt.title("Positive vs Negative Counts of Symptoms")
# plt.grid(True)
# plt.show()










### for plotting +ve vs -ve counts for each symptom ####
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import mplcursors

# # Define the directory containing the CSV files
# directory = '/mnt/0C6C8FC06C8FA2D6/sparse_results_cui'

# # Lists to store aggregated data
# positive_counts = []
# negative_counts = []
# symptom_names = []
# symptom_cui = []

# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         filepath = os.path.join(directory, filename)
        
#         # Load CSV file into a DataFrame
#         df = pd.read_csv(filepath)
        
#         for _, row in df.iterrows():
#             positive_counts.append(row['positive_count'])
#             negative_counts.append(row['negative_count'])
#             symptom_names.append(row['symptom'])
#             symptom_cui.append(row['cui'])

# print(len(symptom_names))

# # Create the scatter plot
# plt.figure(figsize=(10, 6))
# scatter = plt.scatter(positive_counts, negative_counts, alpha=0.5)
# plt.xlabel("Positive Count")
# plt.ylabel("Negative Count")
# plt.title("Positive vs Negative Counts of Symptoms")
# plt.grid(True)

# # Add hover functionality using mplcursors
# cursor = mplcursors.cursor(scatter, hover=True)

# # Define what shows up in the hover text
# @cursor.connect("add")
# def on_add(sel):
#     index = sel.index
#     sel.annotation.set(text=f"Symptom: {symptom_names[index]}\n"
#                             f"CUI: {symptom_cui[index]}\n"
#                             f"Positive Count: {positive_counts[index]}\n"
#                             f"Negative Count: {negative_counts[index]}")

# plt.show()



# ################# for plotting postive/negative ratios ###
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import mplcursors

# # Define the directory containing the CSV files
# directory = '/mnt/0C6C8FC06C8FA2D6/sparse_results_cui'

# # Lists to store aggregated data
# ratios = []
# symptom_names = []
# disease_names = []

# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         # Extract disease name from the filename and replace underscores with spaces
#         disease_name = filename.split('_symptom_counts.csv')[0].replace('_', ' ')
#         filepath = os.path.join(directory, filename)
        
#         # Load CSV file into a DataFrame
#         df = pd.read_csv(filepath)
        
#         for _, row in df.iterrows():
#             symptom_name = row['symptom']
#             positive_count = row['positive_count']
#             negative_count = row['negative_count']
            
#             # Calculate the ratio, handling cases where negative count is zero
#             if negative_count > 0:
#                 ratio = positive_count / negative_count
#             else:
#                 continue
#                 ratio = float('inf')  # Use 'inf' to represent a very high ratio

#             # Append data to lists
#             ratios.append(ratio)
#             symptom_names.append(symptom_name)
#             disease_names.append(disease_name)
        
#     print(len(symptom_names))
#     print(len(disease_names))
#     print(len(ratios))

# # Create the scatter plot
# plt.figure(figsize=(12, 8))
# scatter = plt.scatter(disease_names, ratios, alpha=0.7, color="blue")
# plt.xticks(rotation=90)
# plt.xlabel("Disease")
# plt.ylabel("Positive/Negative Count Ratio")
# plt.title("Positive to Negative Count Ratio for Each Symptom-Disease Pair")
# plt.grid(True)

# # Add hover functionality using mplcursors
# cursor = mplcursors.cursor(hover=True)

# # Define what shows up in the hover text
# @cursor.connect("add")
# def on_add(sel):
#     index = sel.index
#     sel.annotation.set(text=f"Disease: {disease_names[index]}\n"
#                             f"Symptom: {symptom_names[index]}\n"
#                             f"Ratio: {ratios[index]:.2f}")

# plt.tight_layout()
# plt.show()








############# for each pair, plot ratio ###############
import os
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

# Define the directory containing the CSV files
directory = '/mnt/0C6C8FC06C8FA2D6/sparse_results_cui_new'

# Lists to store aggregated data
ratios = []
symptom_names = []
disease_names = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Extract disease name from the filename and replace underscores with spaces
        disease_name = filename.split('_symptom_counts.csv')[0].replace('_', ' ')
        filepath = os.path.join(directory, filename)
        
        # Load CSV file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Assuming the CSV has columns: 'symptom_name', 'positive_count', 'negative_count'
        for _, row in df.iterrows():
            symptom_name = row['symptom']
            positive_count = row['positive_count']
            negative_count = row['negative_count']
            
            # Calculate the ratio, handling cases where negative count is zero
            if negative_count > 0:
                ratio = positive_count / negative_count
            else:
                continue
                ratio = float('inf')  # Use 'inf' to represent a very high ratio

            # Append data to lists
            ratios.append(ratio)
            symptom_names.append(symptom_name)
            disease_names.append(disease_name)

# Map diseases and symptoms to integer positions for plotting
unique_diseases = list(set(disease_names))
unique_symptoms = list(set(symptom_names))
disease_positions = {disease: i for i, disease in enumerate(unique_diseases)}
symptom_positions = {symptom: i for i, symptom in enumerate(unique_symptoms)}

print(len(unique_diseases))
print(len(unique_symptoms))

# Create plot coordinates based on positions
x_coords = [disease_positions[disease] for disease in disease_names]
y_coords = [symptom_positions[symptom] for symptom in symptom_names]

# Create the scatter plot
plt.figure(figsize=(15, 10))
scatter = plt.scatter(x_coords, y_coords, c="blue", alpha=0.6)

# Set x and y ticks with disease and symptom names
plt.xticks(ticks=range(len(unique_diseases)), labels=unique_diseases, rotation=90)
plt.yticks(ticks=range(len(unique_symptoms)), labels=unique_symptoms)

plt.xlabel("Disease")
plt.ylabel("Symptom")
plt.title("Positive to Negative Count Ratio for Each Symptom-Disease Pair")

# Add hover functionality using mplcursors
cursor = mplcursors.cursor(scatter, hover=True)

# Define what shows up in the hover text
@cursor.connect("add")
def on_add(sel):
    index = sel.index
    sel.annotation.set(text=f"Disease: {disease_names[index]}\n"
                            f"Symptom: {symptom_names[index]}\n"
                            f"Ratio: {ratios[index]:.2f}")

plt.tight_layout()
plt.grid(True)
plt.show()

