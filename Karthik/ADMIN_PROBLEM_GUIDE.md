# Admin Guide: Adding Problems with Hidden Test Cases

## Overview

This guide explains how administrators can add programming problems with both sample (visible) and hidden test cases through the Django admin panel.

## Accessing the Admin Panel

1. Go to: http://127.0.0.1:8000/admin/
2. Login with admin credentials:
   - Username: `admin`
   - Password: `gprec@1985`

## Adding a New Problem

### Step 1: Navigate to Problems

1. In the admin panel, find the **LAB** section
2. Click on **Problems**

### Step 2: Add New Problem

1. Click the **"Add Problem"** button (green button at top right)
2. Fill in the problem details:
   - **Title**: Problem title (e.g., "Sum of Two Numbers")
   - **Description**: Detailed problem description
   - **Difficulty**: Select Easy, Medium, or Hard
   - **Is active**: Check to make problem visible to students

### Step 3: Add Test Cases

Scroll down to the **"Test Cases"** section. You'll see an information box explaining how to add test cases.

#### Adding Sample Test Cases (Visible to Students)

1. In the Test Cases section, you'll see empty forms (5 forms for new problems)
2. Fill in the first test case:
   - **Input data**: Test input (e.g., `5 3`)
   - **Expected output**: Expected output (e.g., `8`)
   - **Is sample**: ✅ **CHECK THIS BOX** - This makes it visible to students
   - **Order**: Leave as 0 (or set order if needed)
3. Add 1-2 more sample test cases following the same pattern

#### Adding Hidden Test Cases (For Evaluation Only)

1. In the same Test Cases section, use additional forms
2. Fill in the test case:
   - **Input data**: Test input (e.g., `100 200`)
   - **Expected output**: Expected output (e.g., `300`)
   - **Is sample**: ❌ **UNCHECK THIS BOX** - This makes it hidden from students
   - **Order**: Leave as 0 (or set order if needed)
3. Add multiple hidden test cases to thoroughly test solutions

### Step 4: Save the Problem

1. Click **"Save"** button at the bottom
2. The problem will be created with all test cases

## Understanding Test Case Types

### Sample Test Cases (Is sample = ✅ Checked)

- **Visible to students** when they view the problem
- Help students understand:
  - Input format
  - Expected output format
  - Problem requirements
- **Recommended**: Add 1-3 sample test cases per problem

### Hidden Test Cases (Is sample = ❌ Unchecked)

- **NOT visible to students**
- Used **only for evaluation** when students submit solutions
- Test edge cases, boundary conditions, and various scenarios
- **Recommended**: Add 3-10 hidden test cases per problem

## Example: Complete Problem Setup

### Problem: "Sum of Two Numbers"

**Problem Details:**
- Title: Sum of Two Numbers
- Description: Write a program that takes two integers as input and prints their sum.
- Difficulty: Easy
- Is active: ✅ Checked

**Test Cases:**

1. **Sample Test Case 1** (Visible):
   - Input data: `5 3`
   - Expected output: `8`
   - Is sample: ✅ Checked

2. **Sample Test Case 2** (Visible):
   - Input data: `10 20`
   - Expected output: `30`
   - Is sample: ✅ Checked

3. **Hidden Test Case 1** (Not visible):
   - Input data: `0 0`
   - Expected output: `0`
   - Is sample: ❌ Unchecked

4. **Hidden Test Case 2** (Not visible):
   - Input data: `-5 10`
   - Expected output: `5`
   - Is sample: ❌ Unchecked

5. **Hidden Test Case 3** (Not visible):
   - Input data: `1000000 2000000`
   - Expected output: `3000000`
   - Is sample: ❌ Unchecked

## Viewing Test Case Summary

After saving a problem, you can see:
- **Total test cases**: Total number of test cases
- **Sample (visible)**: Number of test cases visible to students
- **Hidden (evaluation only)**: Number of hidden test cases

This information is displayed in:
1. The problem edit page (in the "Test Cases" section)
2. The problems list page (in the "Test Cases" column)

## Editing Existing Problems

1. Go to Problems list
2. Click on a problem title to edit
3. Scroll to Test Cases section
4. You can:
   - Add new test cases (2 empty forms shown)
   - Edit existing test cases
   - Delete test cases (check "Delete" checkbox)
   - Change test case type (check/uncheck "Is sample")

## Tips for Creating Good Problems

1. **Clear Description**: Write clear, detailed problem descriptions
2. **Sample Test Cases**: Always include 1-3 sample test cases to help students
3. **Hidden Test Cases**: Include multiple hidden test cases covering:
   - Basic cases
   - Edge cases (empty input, zero, negative numbers)
   - Boundary conditions
   - Large inputs
   - Special cases
4. **Exact Output Match**: Ensure expected output matches exactly (including whitespace, newlines)
5. **Test Case Order**: Use the "Order" field to control test case sequence

## Troubleshooting

### Test Cases Not Showing

- Ensure "Is sample" is checked for sample test cases
- Verify problem is saved successfully
- Check that "Is active" is checked

### Students Can't See Sample Test Cases

- Verify "Is sample" is checked for at least one test case
- Ensure problem "Is active" is checked
- Check student is logged in and viewing the correct problem

### Hidden Test Cases Not Evaluating

- Ensure hidden test cases have "Is sample" unchecked
- Verify input and expected output are correctly formatted
- Check that test cases are saved (not just in form)

## Quick Reference

| Action | Is Sample Checkbox |
|--------|-------------------|
| Show to students | ✅ Checked |
| Hide from students (evaluation only) | ❌ Unchecked |

**Remember**: 
- ✅ Checked = Students can see it
- ❌ Unchecked = Students cannot see it (used for evaluation)

