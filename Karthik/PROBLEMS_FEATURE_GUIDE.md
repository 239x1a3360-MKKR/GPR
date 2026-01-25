# Problems Feature Guide

## Overview

The Problems feature allows administrators to create programming problems with test cases that students can solve. Problems can be added manually through the admin panel or imported via CSV files.

## For Administrators

### Adding Problems Manually

1. **Login to Admin Panel**: http://127.0.0.1:8000/admin/
2. **Navigate to Problems**: Click on "Problems" under the "LAB" section
3. **Add New Problem**: Click "Add Problem"
4. **Fill in Details**:
   - **Title**: Problem title
   - **Description**: Detailed problem description
   - **Difficulty**: Easy, Medium, or Hard
   - **Is Active**: Check to make problem visible to students
5. **Add Test Cases**: 
   - Scroll down to "Test cases" section
   - Click "Add another Test case"
   - Fill in:
     - **Input data**: Test input
     - **Expected output**: Expected output
     - **Is sample**: Check if this is a sample test case (shown to students)
     - **Order**: Order of test case
6. **Save**: Click "Save"

### Importing Problems from CSV

1. **Navigate to Problems**: Go to Admin Panel → Problems
2. **Click "Import from CSV"**: Button at the top right
3. **Prepare CSV File**: Use the format below
4. **Upload CSV**: Select your CSV file and click "Import Problems"

#### CSV Format

Your CSV file should have these columns:

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `title` | Yes | Problem title | "Sum of Two Numbers" |
| `description` | Yes | Problem description | "Write a program to add two numbers" |
| `difficulty` | No | easy, medium, or hard | "easy" |
| `is_active` | No | true or false | "true" |
| `test_input` | No | Input for test case | "5 3" |
| `test_output` | No | Expected output | "8" |
| `is_sample` | No | true or false | "true" |

#### Example CSV

```csv
title,description,difficulty,is_active,test_input,test_output,is_sample
"Sum of Two Numbers","Write a program that takes two integers as input and prints their sum.",easy,true,"5 3","8",true
"Factorial","Write a program to calculate the factorial of a number.",medium,true,"5","120",true
```

**Note**: A sample CSV file (`sample_problems.csv`) is included in the project root.

### Managing Test Cases

- **Sample Test Cases**: These are visible to students and help them understand the problem
- **Hidden Test Cases**: Uncheck "Is sample" to create hidden test cases for evaluation
- **Multiple Test Cases**: Add multiple test cases per problem for thorough evaluation

## For Students

### Viewing Problems

1. **Login**: http://127.0.0.1:8000/
2. **Click "Problems"**: In the navigation bar
3. **Filter**: Use difficulty filter to find problems
4. **Select Problem**: Click on a problem to view details

### Solving Problems

1. **Read Problem**: Read the description and sample test cases
2. **Write Code**: Use the code editor to write your solution
3. **Select Language**: Choose from C, C++, Java, or Python
4. **Submit Solution**: Click "Submit Solution"
5. **View Results**: 
   - See test case results
   - View passed/failed test cases
   - Check your submission history

### Submission Status

- **Accepted**: All test cases passed
- **Partial**: Some test cases passed
- **Failed**: No test cases passed
- **Error**: Code compilation/runtime error

## Features

### Automatic Evaluation

- Code is automatically evaluated against all test cases
- Results show which test cases passed/failed
- Sample test cases are shown to students
- Hidden test cases are used for evaluation only

### Submission Tracking

- All submissions are saved
- View submission history for each problem
- See test case results for each submission
- Track progress over time

### Admin Features

- View all submissions
- Filter by problem, user, language, status
- Review code and test results
- Manage problems and test cases

## Best Practices

### For Problem Creation

1. **Clear Descriptions**: Write clear, detailed problem descriptions
2. **Sample Test Cases**: Always include sample test cases
3. **Multiple Test Cases**: Include edge cases and various scenarios
4. **Difficulty Levels**: Set appropriate difficulty levels
5. **Test Output Format**: Ensure expected output matches exactly (including whitespace)

### For CSV Import

1. **Validate CSV**: Check CSV format before importing
2. **Test Import**: Import a few problems first to test
3. **Backup**: Keep a backup of your CSV files
4. **Encoding**: Use UTF-8 encoding for CSV files

## Troubleshooting

### CSV Import Fails

- Check CSV format matches the required columns
- Ensure required fields (title, description) are present
- Verify CSV encoding is UTF-8
- Check for special characters in CSV

### Test Cases Not Working

- Ensure expected output matches exactly (including newlines, spaces)
- Check input/output format matches your problem description
- Verify test cases are properly saved in admin panel

### Submissions Not Evaluating

- Check that problem has test cases
- Verify code execution is working
- Check server logs for errors

## Example Problems

See `sample_problems.csv` for example problems that can be imported.

