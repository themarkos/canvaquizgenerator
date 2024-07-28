import os
import csv
import anthropic
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the output folder path
output_folder_path = r"CHOOSE OUTPUT FOLDER"

# Authenticate with the Anthropic API using your API key
client = anthropic.Client(api_key="YOUR CLAUDE 3 Haiku API")

# Specify the Claude model to use
model = "claude-3-haiku-20240307"

def make_api_call(prompt):
    messages = [{"role": "user", "content": prompt}]
    
    try:
        logging.info("Connecting to API")
        response = client.messages.create(
            model=model,
            messages=messages,
            max_tokens=4000,
            stop_sequences=["\n\nHuman:"],
        )
        result = response.content[0].text
        logging.info("Successfully connected to API")
        return result
    except Exception as e:
        logging.error(f"API request failed: {str(e)}")
        return None

def save_to_csv(result, output_file):
    try:
        # Split the result into rows
        rows = [row.strip().split('|') for row in result.strip().split('\n')]
        
        # Remove any empty strings from each row
        rows = [[cell.strip() for cell in row if cell.strip()] for row in rows]
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
        logging.info(f"Saved response to CSV: {output_file}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")

def main():
    # Your prompt that will generate a table response
    prompt = """Create me 50 sets of questions and answers in the same style as the below is the context to use, and format them in a table where one column is the question, with a max word count of 14. Part 2 is the third column which is always the correct answer for the question. Column two, four and five which is Part 1 and Part 3 and Part 4 is the wrong answers to the question. The max character count for Part 1, 2, 3, 4 is 21. These should be questions and answers about ENTER NICHE. Keep the questions engaging, polarizing, over the top and relatable to everyone or people who ARE IN THE NICHE. The reading grade should be under grade 10 ideally Here is content to make the questions and answers:
    """
    
    # Make API call
    result = make_api_call(prompt)

    # Save the result to CSV
    if result:
        output_file = os.path.join(output_folder_path, "output_table.csv")
        save_to_csv(result, output_file)

    logging.info("Process completed.")

if __name__ == "__main__":
    main()