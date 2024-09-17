import os
import sys
import django
from bs4 import BeautifulSoup, Doctype, Comment, ProcessingInstruction
import json
from django.core.files import File
import re


# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
print(current_directory)
print("ppppppppPPPPPPPPPP00000")

from webpage.models import ImageFile, Language, PageData  # Update with your app name

def extract_color_from_style(style):
    style = style.lower()
    color = "no color"
    if 'color:' in style:
        start = style.find('color:') + len('color:')
        end = style.find(';', start)
        color = style[start:end].strip()
    return color

def extract_background_color_from_style(style):
    style = style.lower()
    bg_color = ""
    if 'background-color:' in style:
        start = style.find('background-color:') + len('background-color:')
        end = style.find(';', start)
        bg_color = style[start:end].strip()
    return bg_color

def get_text_type(tag):
    if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
        return 'header'
    elif tag.name == 'p':
        return 'paragraph'
    elif tag.name == 'li':
        return 'list'
    else:
        return 'other'

def parse_html(file_path, page_data, static_folder, output_folder):
    print(file_path)
    print("$$$$")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    data = {
        "texts": [],
        "images": [],
        "links": [],
        "divs": []
    }
    
    tag_id_counter = 1

    # Extract text elements (excluding those inside <a> tags)
    for tag in soup.find_all(string=True):
        if isinstance(tag, (Doctype, Comment, ProcessingInstruction)):
            continue
        if tag.string and tag.parent.name not in ['script', 'style', 'a']:
            text_content = tag.string.strip()
            if text_content and '{{' not in text_content and '{%' not in text_content:
                tag_id = f"text_{tag_id_counter}"
                tag.parent['id'] = tag_id
                text_type = get_text_type(tag.parent)
                style = tag.parent.get('style', 'no style')
                data["texts"].append({
                    "id": tag_id,
                    "text": text_content,
                    "color": extract_color_from_style(style),
                    "text_style": style,
                    "type": text_type
                })
                tag_id_counter += 1
    
    
    # Extract link elements
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            src = a.get('href')
            if "{%" not in src:
                link_text = a.string.strip() if a.string else ""
                if link_text:
                    if ".html" in src:
                        tag_id = f"link_{tag_id_counter}"
                        a['id'] = tag_id
                        data["links"].append({
                            "id": tag_id,
                            "name": link_text,
                            "link": f"/pages/{a.get('href')}/"
                        })
                        tag_id_counter += 1
                    else:
                        tag_id = f"link_{tag_id_counter}"
                        a['id'] = tag_id
                        data["links"].append({
                            "id": tag_id,
                            "name": link_text,
                            "link": f"/{a.get('href')}/"
                        })
                        tag_id_counter += 1



    # Extract div elements for background color
    for div in soup.find_all('div'):
        tag_id = f"div_{tag_id_counter}"
        src = a.get('id')
        if src:
            if "loginForm" not in src and "registerForm" not in src:
                div['id'] = tag_id
                bg_color = extract_background_color_from_style(div.get('style', ''))
                data["divs"].append({
                    "id": tag_id,
                    "background_color": bg_color
                })
                tag_id_counter += 1
        else:
        
            div['id'] = tag_id
            bg_color = extract_background_color_from_style(div.get('style', ''))
            data["divs"].append({
                "id": tag_id,
                "background_color": bg_color
            })
            tag_id_counter += 1

    # Extract image elements and register them in the ImageFile model
    for img in soup.find_all('img'):
        src = img.get('src')
        if src.startswith("{% static '") and src.endswith("' %}"):
            src = src[11:-4]  # Remove "{% static '" from the beginning and "' %}" from the end
        print(src)
        print("0000")
        if src.startswith("http://") or src.startswith("https://"):
            continue
        if "{{" not in src and "{%" not in src:
            try:
                full_image_path77 = os.path.join('static', src)
                tag_id = f"image_{tag_id_counter}"
                img['id'] = tag_id
                description = img.get('alt', '')
                width = img.get('width', 400)
                height = img.get('height', 700)

                        # Construct the path to the file using Django's default storage

                # Ensure the file exists and is safe to access
                if not os.path.exists(full_image_path77):
                    raise FileNotFoundError(f"File not found: {full_image_path77}")

                with open(full_image_path77, 'rb') as f:
                    django_file = File(f)
                    image_instance = ImageFile.objects.create(
                        description=description, file= django_file,width= width,height = height)

                page_data.images.add(image_instance)

                data["images"].append({
                    "id": tag_id,
                    "imgid":image_instance.id,
                    "src": image_instance.file.url
                })
                tag_id_counter += 1
            except FileNotFoundError as e:
                print(f"File not found 1: {full_image_path77}")
                continue 

    # Process background-image styles
    for element in soup.find_all(style=re.compile(r'background-image:')):
        style = element.get('style')
        match = re.search(r'url\((.*?)\)', style)
        if match:
            src = match.group(1).strip('\'"')
            if src.startswith("{% static '") and src.endswith("' %}"):
                src = src[11:-4] 
            if "{%" not in src and "{{" not in src:
                try:
                    full_image_path = os.path.join('static', src)
                    print(src)
                    tag_id = f"bg_image_{tag_id_counter}"
                    element['id'] = tag_id

                   
                    with open(full_image_path, 'rb') as f:
                        django_file = File(f)
                        image_instance = ImageFile.objects.create(
                            description='Background image', file=django_file)

                    page_data.images.add(image_instance)

                    data["images"].append({
                        "id": tag_id,
                        "imgid": image_instance.id,
                        "src": image_instance.file.url
                    })
                    tag_id_counter += 1
                except FileNotFoundError as e:
                    print(f"File not found 2: {full_image_path}")
                    continue 

    json_data = json.dumps(data, indent=4)

    # Save JSON data to the Language model
    language = Language.objects.create(code='en', name='English', data = json_data)
    language.save()
    page_data.languages.add(language)


    # Add a placeholder script tag for JSON data
    placeholder_tag = soup.new_tag('script', type='application/json', id='templateData')
    placeholder_tag.string = '{{ json_data|safe }}'
    print("lllllllll")
    print(placeholder_tag)
    soup.body.append(placeholder_tag)


    # Create a script tag for the JS function
    script_tag_js = soup.new_tag('script')
    script_tag_js.string = f"""
        function updateHtmlFromJson(jsonData) {{
            // Update text tags
            jsonData.texts.forEach(tag => {{
                const element = document.getElementById(tag.id);
                if (element) {{
                    element.textContent = tag.text;
                    if (tag['text_style'] !== 'no style') {{
                        element.style.fontFamily = tag['text_style'];
                    }}
                    if (tag.color !== 'no color') {{
                        element.style.color = tag.color;
                    }}
                }}
            }});

            // Update images
            jsonData.images.forEach(image => {{
                const element = document.getElementById(image.id);
                if (element) {{
                    element.src = image.src;
                     if (element.tagName.toLowerCase() === 'img') {{
                        element.src = image.src;
                    }}else {{
                        element.style.backgroundImage = `url(${{image.src}})`;
                    }}
                }}
            }});

            // Update links
            jsonData.links.forEach(link => {{
                const element = document.getElementById(link.id);
                if (element) {{
                    element.textContent = link.name;
                    element.href = link.link;
                }}
            }});

            // Update div background colors
            jsonData.divs.forEach(div => {{
                const element = document.getElementById(div.id);
                if (element) {{
                    element.style.backgroundColor = div.background_color;
                }}
            }});
        }}

        // Fetch JSON data from templateData
        const jsonData = JSON.parse(document.getElementById('templateData').textContent);

        // Call the function to update HTML elements
        document.addEventListener('DOMContentLoaded', () => {{
            updateHtmlFromJson(jsonData);
        }});
    """
    soup.body.append(script_tag_js)

    
    script_tag_js2 = soup.new_tag('script')
    script_tag_js2.string ="""
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('[id]').forEach(element => {
        element.addEventListener('click', function () {
          const id = this.id;
          window.flutter_inappwebview.callHandler('Toaster', id);
        });
      });
    });
    """
    soup.body.append(script_tag_js2)

    

    # Save updated HTML file in the output folder
    output_file_path = os.path.join(output_folder, os.path.basename(file_path))
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    # Update the paths in the HTML file
    update_html_paths(output_file_path)

    return data

# Function to update HTML file paths for static files and add necessary tags
def update_html_paths(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Add {% load static %}{% load custom_tags %} at the beginning of the file
    load_tags = BeautifulSoup('{% load static %}{% load custom_tags %}{% load myapp_tags %}\n', 'html.parser')
    if soup.contents:
        soup.insert(0, load_tags)
    else:
        soup.append(load_tags)

    # Update CSS paths
    for link in soup.find_all('link', rel='stylesheet'):
        if link.get('href'):
            sr =  link.get('href')
            if "https" not in sr:
                link['href'] = "{% static '" + link['href'] + "' %}"

    # Update JS paths
    for script in soup.find_all('script'):
        if script.get('src'):
            sr =  script.get('src')
            if "https" not in sr:
                script['src'] = "{% static '" + script['src'] + "' %}"

    # Update image paths
    for img in soup.find_all('img'):
        if img.get('src'):
            sr =  img.get('src')
            if "{{" not in sr and "{%" not in sr:
                img['src'] = "{% static '" + img['src'] + "' %}"

    # Update background-image paths in inline styles
    for tag in soup.find_all(style=True):
        style = tag.get('style')
        if 'background-image' in style or 'background:' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            background_image_url = style[url_start:url_end].strip('\'"')
            if "{{" not in background_image_url and "{%" not in background_image_url:
                new_style = style.replace(background_image_url, "{% static '" + background_image_url + "' %}")
                tag['style'] = new_style

    # Add JSON data script tag if it doesn't exist
    if not soup.find('script', {'id': 'templateData'}):
        script_tag = soup.new_tag("script", type="application/json", id="templateData")
        script_tag.string = '{{ json_data|safe }}'
        soup.body.append(script_tag)

    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def process_folder(folder_path, static_folder, output_folder):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            file_path1 = os.path.join('pages', filename)
            # Create or get the PageData entry
            page_name = os.path.splitext(filename)[0]
            page_data, created = PageData.objects.get_or_create(
                page_name=filename,
                defaults={'template_location': file_path1}
            )
            data = parse_html(file_path, page_data, static_folder, output_folder)
            all_data.append(data)
    return all_data

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python convert_html.py <folder_path> <static_folder> <output_folder>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    static_folder = sys.argv[2]
    output_folder = sys.argv[3]
    all_data = process_folder(folder_path, static_folder, output_folder)
