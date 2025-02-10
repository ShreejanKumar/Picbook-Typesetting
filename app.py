import streamlit as st
from main import get_response, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers, image_html, html_latex
import os
from io import BytesIO


# Streamlit UI
st.title("Chapter PDF Generator")

def get_word_count(html_file_path):
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text from the HTML
    text = soup.get_text()
    
    # Split the text into words and count them
    words = text.split()
    word_count = len(words)
    
    return word_count

# Dynamic list to store chapter inputs
# os.system('playwright install')
chapter_texts = []
num_chapters = st.number_input('How many chapters do you want to add?', min_value=1, max_value=10, step=1)
images = []
image_description = []
for i in range(num_chapters):
    # Chapter text input
    chapter_text = st.text_area(f'Enter the Chapter {i+1} text:', key=f'chapter_text_{i}')
    chapter_texts.append(chapter_text)

    # Word count display
    word_count = len(chapter_text.split()) if chapter_text else 0
    st.write(f'Word count: {word_count}')

    # Number of images for the chapter
    num_images = st.number_input(f'How many images for Chapter {i+1}?', min_value=1, max_value=10, step=1, key=f'num_images_{i}')

    # List to store images for the current chapter
    chp_image = []
    img_descp = []
    for j in range(num_images):
        img_link = st.text_input(f"Enter Google drive link of Image {j+1} for Chapter {i+1}", key=f'img_link_{i}_{j}')
        temp_desc = st.text_input(f'Enter the Image {j+1} description:', key=f'img_desc_{i}_{j}')
        chp_image.append(img_link)
        img_descp.append(temp_desc)

    image_description.append(img_descp)
    # Append chapter images to images list
    images.append(chp_image)
    
author_name = st.text_input('Enter the Author Name:')
book_name = st.text_input('Enter the Book Name:')
font_size = st.text_input('Enter the Font Size')
line_height = st.text_input('Enter the Line Spacing')

# Dropdown menu for font selection
fonts = [
    'Courier', 'Courier-Bold', 'Courier-BoldOblique', 'Courier-Oblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-BoldOblique', 'Helvetica-Oblique',
    'Times-Roman', 'Times-Bold', 'Times-BoldItalic', 'Times-Italic',
    'Symbol', 'ZapfDingbats'
]
font_style = st.selectbox('Select Font Style:', fonts)

# First_page_no = st.number_input('Enter the First Page Number:', min_value=0, max_value=1000, step=1)
options = ['Left', 'Right']
# first_page_position = st.selectbox('Select First Page Position:', options)
orient = ['Portrait', 'Landscape']
orientation = st.selectbox('Select Orientation', orient)

# Button to generate PDF
if st.button("Generate PDF"):
    final_pdfs = []
    # current_page_number = First_page_no  # Start from the user-defined first page number

    # Set the initial page position for the first chapter
    # current_position = first_page_position  # "Right" or "Left" based on input
    wc = []
    for idx, chapter_text in enumerate(chapter_texts):
        response = get_response(chapter_text, font_size, line_height)
        if idx < len(images) and idx < len(image_description):  # Ensure images and descriptions exist for the current chapter
            for img_idx, (image_path, image_desc) in enumerate(zip(images[idx], image_description[idx])):
                # Update the response iteratively with each image and description
                response = image_html(response, image_path, image_desc, orientation)  # Update `response` directly
        latex = html_latex(response)
        html_pth = save_response(response)
    #     wc.append(get_word_count(html_pth))
    #     main_pdf = f'out_{idx+1}.pdf'
        
    #     # Run the function to generate the main PDF
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf, orientation))

    #     total_pages = get_pdf_page_count(main_pdf)
    #     overlay_pdf = f"overlay_{idx+1}.pdf"
        
    #     # Create the overlay PDF with continuous page numbers
    #     current_position = create_overlay_pdf(overlay_pdf, total_pages, current_page_number, book_name, author_name, font_style, current_position)
        
    #     final_pdf = f'final_{idx+1}.pdf'
    #     final_pdfs.append(final_pdf)
        
    #     # Overlay the headers and footers
    #     overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)
        
    #     # Update current_page_number for the next chapter
    #     current_page_number += total_pages
    
    # # Merge all the final PDFs into one
    # merger = PdfMerger()
    # for pdf in final_pdfs:
    #     merger.append(pdf)

    # merged_pdf_path = 'merged_final.pdf'
    # merger.write(merged_pdf_path)
    # merger.close()

    # st.success("All PDFs merged successfully into one!")

    # # Provide a download button for the merged final PDF
    # with open(merged_pdf_path, "rb") as pdf_file:
    #     st.download_button(
    #         label="Download Final Merged PDF",
    #         data=pdf_file,
    #         file_name=merged_pdf_path,
    #         mime="application/pdf"
    #     )
    # st.write(wc)