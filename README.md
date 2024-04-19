The script creates (if they don't exist) three folders:
  - "input_folder" - a folder for input data saved in JSON format.
  - "output_folder" - a folder for output data saved in XML format.
  - "processed_folder" - a folder for correctly processed data in JSON format moved from the "input_folder".
  
Here's how the script works:
  - The script converts JSON files from the input folder to XML format and then moves them to the output folder.
  - It ensures that the input file is fully saved before conversion.
  - Error handling prevents the flow from being blocked in case of issues.
  - Folder monitoring is done in a loop, regularly checking for the presence of JSON files in the input folder.
