import tabula

# Path to your pdf
pdf_path = "example.pdf"

page_height_cm = 21.58

def cm_to_pts(cm):
    return (cm / 2.54) * 72


# Calculate from bottom of the page
top = cm_to_pts(2.69)
bottom = cm_to_pts(page_height_cm - 11.76)  # 10.77cm from bottom
left = cm_to_pts(1.92)
right = cm_to_pts(11.45)

# This assumes a page size of approximately 800x600 points,
# top, left, bottom, right
area = [top, left, bottom, right]
# Read pdf into list of DataFrame
dfs = tabula.read_pdf(pdf_path, pages='all', area=area, multiple_tables=True)

# Print the extracted table data
if dfs:
    for df in dfs:
        print(df)
else:
    print("No tables found.")

# tabula.convert_into(pdf_path, "output.csv", output_format="csv", pages='all')
