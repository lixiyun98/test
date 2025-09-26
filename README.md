# test

## Filename Analysis Script

This repository contains a Python script that analyzes JSON filenames and generates statistics.

### analyze_filenames.py

Analyzes JSON files with the pattern `{uuid}_{status}.json` where status is either "correct" or "incorrect".

**Features:**
- Extracts UUID and status from filenames
- Handles priority logic: "correct" status takes precedence over "incorrect" for the same UUID
- Generates JSON output with UUID->status mapping
- Provides detailed logging and error handling

**Usage:**
```bash
# Use default directory (/Users/xiyunli/owl/result/hunyuan/level_1_details)
python3 analyze_filenames.py

# Specify custom directory
python3 analyze_filenames.py /path/to/directory
```

**Output:**
- Creates `file_statistics.json` with the results
- Displays processing statistics and summary

**Example:**
For files:
- `cffe0e32-c9a6-4c52-9877-78ceb4aaa9fb_incorrect.json`
- `550e8400-e29b-41d4-a716-446655440000_correct.json`
- `550e8400-e29b-41d4-a716-446655440000_incorrect.json`

Output JSON:
```json
{
  "550e8400-e29b-41d4-a716-446655440000": "correct",
  "cffe0e32-c9a6-4c52-9877-78ceb4aaa9fb": "incorrect"
}
```

<img>