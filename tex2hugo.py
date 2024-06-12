#%%
import re
import os
import shutil
import datetime

from pdf2image import convert_from_path
import os

def pdf2png(pdf_file, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(pdf_file)
    
    # Convert PDF to list of images
    images = convert_from_path(pdf_file)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each image
    for i, image in enumerate(images, start=1):
        image.save(os.path.join(output_dir, pdf_file.replace(".pdf",".png")), 'PNG')
        print()

def convert_figure(match, fig_dir, outfigdir):
    figure_content = match.group(1)
    figure_content = re.sub(r'\\includegraphics\[.*?\]{(.*?)}\n', lambda match: convert_image(match, fig_dir, outfigdir), figure_content)
    figure_content = re.sub(r'\\caption{(.*?)}\n', r'caption="\1"', figure_content)
    figure_content = figure_content.replace('\n', ' ')
    figure_content = re.sub(r'\s+', ' ', figure_content)
    
    # Convert consecutive spaces to a single space
    figure_content = figure_content.replace('\\centering', '')
    # Remove \centering
    return r'{{< figure '+figure_content+r' >}}'

def convert_image(match, fig_dir, outfigdir):
    image_path = os.path.basename(match.group(1))
    if image_path.endswith('.pdf'):
        image_path = image_path.replace('.pdf','.png')
    elif image_path.endswith('.eps'):
        image_path = image_path.replace('.eps','.png')
    project_dir = os.path.join(
            os.path.basename(os.path.dirname(outfigdir)),
            os.path.basename(outfigdir),
        )
    image_path = os.path.join(f"https://raw.githubusercontent.com/is-enaga/mynote/main/{project_dir}", image_path)
    # print(project_dir)
    return f'src="{image_path}"'


def tex2hugo(tex_file, fig_dir, output_dir, outfigdir=None):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(tex_file, 'r') as f:
        tex_content = f.read()
    
    # Remove everything before the first chapter
    tex_content = re.sub(r'^.*?\n\\chapter', r'\\chapter', tex_content, flags=re.DOTALL)
    
    # Split the content into chapters
    chapters = re.split(r'\\chapter', tex_content)

    for i, chapter in enumerate(chapters[1:], start=1):  # Skip the first element (empty)
        
        # Extract the chapter title
        chapter_title = re.search(r'{(.*?)}', chapter).group(1)
        
        if chapter_title=="索引":
            continue
        
        chapter = re.sub(
            r'{(.*?)}', 
            rf'# 第{i}章　\1',
            # rf'---\ntitle: 第{i}章　\1 \ndate: {datetime.datetime.now().strftime("%Y-%m-%d")}\nweight: {i*10} \n---\n\n',
            chapter, count=1)
        # chapter = re.sub(
        #     r'{(.*?)}',
        #     fr'---\ntitle: 第{i}章　{chapter_title}\n---\n',
        #     chapter,
        #     count=1,)
        
        
        # Remove index
        chapter = re.sub(r'\\index{(.*?)}', '', chapter)
        
        # Remove ref
        chapter = re.sub(r'\\ref{(.*?)}', r'*※相互参照無効*', chapter)
        
        # Convert URLs
        chapter = re.sub(r'\\url{(.*?)}', r'[\1](\1)', chapter)
        
        # Convert labels
        chapter = re.sub(r'\\label{(.*?)}', '', chapter)
        
        # Remove head and foot \pagenumbering{arabic}
        chapter = re.sub(r'\\pagenumbering{arabic}', '', chapter)
        chapter = re.sub(r'\\printindex', '', chapter)
        chapter = re.sub(r'\\tableofcontents', '', chapter)
        chapter = re.sub(r'\\clearpage', '', chapter)
        chapter = re.sub(r'\\newpage', '', chapter)
        chapter = re.sub(r'\\pagebreak', '', chapter)
        chapter = re.sub(r'\\vspace{.*?}', '', chapter)
        chapter = re.sub(r'\\hspace{.*?}', '', chapter)
        chapter = re.sub(r'\\end{document}', '', chapter)
        
        
        # ----------------------
        # Convert section headings
        # ----------------------
        chapter = re.sub(r'\\section{(.*?)}', r'## \1', chapter)
        chapter = re.sub(r'\\subsection{(.*?)}', r'### \1', chapter)
        chapter = re.sub(r'\\subsubsection{(.*?)}', r'#### \1', chapter) 
        
        # ----------------------
        # Convert code blocks
        # ----------------------
        chapter = re.sub(r'\\begin{verbatim}(.*?)\\end{verbatim}', r'```plaintext\n\1 ```\n\n', chapter)
        chapter = chapter = re.sub(r'\\begin{lstlisting}\[.*?\](.*?)\\end{lstlisting}', r'```python\n\1```\n', chapter, flags=re.DOTALL)
        
        # inline code
        chapter = re.sub(r'\\code{(.*?)}', r'`\1`', chapter)
        
        # ----------------------
        # Convert equations
        # ----------------------
        # Convert display equations
        chapter = re.sub(r'\\begin{equation\*}(.*?)\\end{equation\*}', r'{{< math >}}\n$$\1$$\n{{< /math >}}', chapter)
        chapter = re.sub(r'\\begin{equation}(.*?)\\end{equation}', r'{{< math >}}\n$$\1$$\n{{< /math >}}', chapter)
        chapter = re.sub(r'\\begin{align}(.*?)\\end{align}', r'{{< math >}}\n$$\1$$\n{{< /math >}}', chapter)
        chapter = re.sub(r'\\begin{align\*}(.*?)\\end{align\*}', r'{{< math >}}\n$$\1$$\n{{< /math >}}', chapter)
        
        # Convert inline equations
        # chapter = re.sub(r'\$(.*?)\$', r'{{< math >}} $\1$ {{< /math >}}', chapter)

        # Split the text into code blocks and non-code blocks
        parts = re.split(r'(```.*?```)', chapter, flags=re.DOTALL)
        # Apply the appropriate transformations to each part
        for _i in range(len(parts)):
            if i % 2 == 0:  # This is a non-code block
                parts[_i] = re.sub(r'\$(.*?)\$', r'{{< math >}} $\1$ {{< /math >}}', parts[_i])
            # else: This is a code block, so we don't apply any transformations

        # Rejoin the parts into a single string
        chapter = ''.join(parts)



        # ----------------------
        # Convert figures for hugo
        # ----------------------
        # Convert
        chapter = re.sub(r'\\begin{figure}\[.*?\](.*?)\\end{figure}', lambda match: convert_figure(match, fig_dir, outfigdir), chapter, flags=re.DOTALL)

        
        # Convert comments
        chapter = re.sub(r'\s*%(.*?)\n', r'\n<!-- \1 -->\n', chapter)
        
        # Convert \\
        chapter = re.sub(r'\\\\', r'  ', chapter)
        
        # ----------------------
        # Convert tcolorbox
        # ----------------------
        chapter = re.sub(r'\\begin{tcolorbox}\[.*?\](.*?)\\end{tcolorbox}', r'{{% callout note %}}\n\1\n{{% /callout %}}\n\n', chapter, flags=re.DOTALL)
        
        
        # ----------------------
        # Convert items
        # ----------------------
        # Enumerate
        def convert_enumerate(match):
            enumerate_content = match.group(1)
            converted_content = re.sub(r'\\item', '###', enumerate_content)
            converted_content = re.sub(r'\n\s+', '\n', converted_content)
            return '{{% steps %}}\n' + converted_content + '\n{{% /steps %}}'

        chapter = re.sub(r'\\begin{enumerate}(.*?)\\end{enumerate}', lambda match: convert_enumerate(match), chapter, flags=re.DOTALL)
        
                        
        # Convert itemize
        # def convert_itemize(match):
        #     itemize_content = match.group(1)
        #     converted_content = re.sub(r'\\item', '-', itemize_content)
        #     converted_content = re.sub(r'\n\s+', '\n', converted_content)
        #     return '\n' + converted_content + '\n'
        def convert_itemize(match):
            itemize_content = match.group(1)
            converted_content = re.sub(r'\\item\[(.*?)\]', r'- \1', itemize_content)
            converted_content = re.sub(r'\\item', '-', converted_content)
            converted_content = re.sub(r'\n\s+', '\n', converted_content)
            return '\n' + converted_content + '\n'
        chapter = re.sub(r'\\begin{itemize}(.*?)\\end{itemize}', lambda match: convert_itemize(match), chapter, flags=re.DOTALL)        
        
        
        # Write the chapter to a separate Markdown file
        md_file = os.path.join(output_dir, f'sec{i:03.0f}.md')
        with open(md_file, 'w') as f:
            f.write(chapter)

        print(f'Chapter {i}: {chapter_title} converted to {md_file}')

    # =======================
    # figure
    # =======================
    if os.path.exists(fig_dir):
        if outfigdir is None:
            outfigdir = os.path.join(
                output_dir,
                os.path.basename(fig_dir),
                )
        # Copy figdir to the output directory
        os.makedirs(outfigdir, exist_ok=True)
        
        # Copy the contents of fig_dir to the output directory
        shutil.copytree(fig_dir, outfigdir, dirs_exist_ok=True)
        
        # Convert PDF files to PNG and save them in the output directory
        pdf_files = [file for file in os.listdir(fig_dir) if file.endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(outfigdir, pdf_file)
            pdf2png(pdf_path, outfigdir)
    
    return




# %%
# %%
