import os
import json
from bs4 import BeautifulSoup
import sys
from imageupload import *  # Import your image upload function
import re



# Replace with your actual model

text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']

def add_ids_to_tags(soup, tag_names):
    for tag_name in tag_names:
        tags = soup.find_all(tag_name)
        for index, tag in enumerate(tags):
            tag_id = f"{tag_name}_{index + 1}"
            tag['id'] = tag_id

def update_html_template(template_content, generated_js_code):
    soup = BeautifulSoup(template_content, 'html.parser')

    # Add {% load static %} and {% load custom_tags %} at the beginning
    load_static_tag = soup.new_tag('script')
    load_static_tag.string = "{% load static %}"
    load_custom_tags_tag = soup.new_tag('script')
    load_custom_tags_tag.string = "{% load custom_tags %}"
    soup.head.insert(0, load_static_tag)
    soup.head.insert(1, load_custom_tags_tag)

    # Add <script>var jsonDataww = {{ json_data|safe }};</script> at the top
    json_script_tag = soup.new_tag('script')
    json_script_tag.string = "var jsonDataww = {{ json_data|safe }};"
    soup.head.insert(2, json_script_tag)

    # Add {% render_login_modal logstat chat_id %}
    render_login_modal_tag = soup.new_tag('div')
    render_login_modal_tag.string = "{% render_login_modal logstat chat_id %}"
    soup.body.insert_before(render_login_modal_tag)

    # Replace static file paths with {% static %} template tags
    for link_tag in soup.find_all('link'):
        if 'href' in link_tag.attrs:
            href = link_tag['href']
            if href.startswith('/static/'):
                link_tag['href'] = f"{{% static '{href[len('/static/'):]} %}}"
            else:
                link_tag['href'] = f"{{% static '{href}' %}}"

    for script_tag in soup.find_all('script'):
        if 'src' in script_tag.attrs:
            src = script_tag['src']
            if src.startswith('/static/'):
                script_tag['src'] = f"{{% static '{src[len('/static/'):]} %}}"
            else:
                script_tag['src'] = f"{{% static '{src}' %}}"

    # Replace href attributes with {% static %} template tags
    for link_tag in soup.find_all('link', href=True):
        if link_tag['href'].startswith('assets/'):
            link_tag['href'] = f"{{% static '{link_tag['href']}' %}}"

    # Replace src attributes with {% static %} template tags
    for script_tag in soup.find_all('script', src=True):
        if script_tag['src'].startswith('assets/'):
            script_tag['src'] = f"{{% static '{script_tag['src']}' %}}"

    # Add <script src="{% static 'webfunction.js' %}"></script> before </body>
    script_tag = soup.new_tag('script', src="{% static 'webfunction.js' %}")
    soup.body.append(script_tag)

    # Remove text content from specific tags as before
    text_tags0 = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']

    for tag in soup.find_all(text_tags0):
        tag.string = ""

    generated_js_tag = soup.new_tag('script')
    generated_js_tag.string = generated_js_code
    soup.body.append(generated_js_tag)

    return str(soup)

def generate_json_data(soup, tag_names):
    json_data = {}

    for tag_name in tag_names:
        if tag_name == 'a':
            link_tags = soup.find_all('a')

            # Extract and print the links and icons
            for link in link_tags:
                if 'id' in link.attrs:
                    tag_id = link['id']
                    href = link.get('href') 
                    # Check if the link contains an icon represented as an HTML element
                    icon_tag = link.find('i') or link.find('span') or link.find('svg')
                    if href and icon_tag:
                        icon_html = icon_tag.prettify()  # Get the HTML of the icon
                        text = link.get_text().strip()  # Get the text within the <a> tag
                        print(f"Link: {href}, Text: {text}, Icon: {icon_html}")
                        link_a = {}
                        link_a['link'] = href
                        link_a['text'] = f"{text}{icon_html}"
                        json_data[tag_id] = link_a

        else:
            tags = soup.find_all(tag_name)
            for index, tag in enumerate(tags):
                if 'id' in tag.attrs:
                    tag_id = tag['id']
                    json_data[tag_id] = tag.get_text().strip()

    return json_data

def process_html_file(input_html_path):
    current_script_path = os.path.abspath(__file__)
    template_directory = os.path.join(os.path.dirname(current_script_path), 'templets')
    print(template_directory)
    # Save the main.html file in the template directory
    output_html_path = os.path.join(template_directory, 'main.html')

    with open(input_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Adding IDs to text-containing tags
    add_ids_to_tags(soup, text_tags)

    '''img_tags = soup.find_all('img')
    for index, img_tag in enumerate(img_tags):
        impath = os.path.dirname(input_html_path)
        img_path = os.path.join(impath, img_tag['src'])
        image_id = upload_image_to_model(img_path)
        img_tag['src'] = f"{{% get_image_url {image_id} %}}"
    '''


    # Regex pattern to extract URL from style attribute
    url_pattern = re.compile(r"url\(['\"]?(.*?)['\"]?\)")

    img_tags = soup.find_all(['img', lambda tag: 'style' in tag.attrs])
    for index, tag in enumerate(img_tags):
        if tag.name == 'img':
            src = tag['src']
        elif 'background-image' in tag['style']:
            match = url_pattern.search(tag['style'])
            if match:
                src = match.group(1)
            else:
                continue  # Skip if no URL found
        else:
            continue  # Skip if not an image or background image
            
        impath = os.path.dirname(input_html_path)
        img_path = os.path.join(impath, src)
        image_id = upload_image_to_model(img_path)
        if tag.name == 'img':
            tag['src'] = f"{{% get_image_url {image_id} %}}"
        else:
            tag['style'] = tag['style'].replace(src, f"{{% get_image_url {image_id} %}}")


    generated_js_code = """
    document.addEventListener('DOMContentLoaded', function () {
        // Iterate over each key in the JSON data
        for (var key in jsonDataww) {
            if (jsonDataww.hasOwnProperty(key)) {
                var element = document.getElementById(key);
                if (element) {
                    if(key.startsWith("a")){
                        element.href = jsonDataww[key['link']];
                    }else{
                        element.textContent = jsonDataww[key];
                    }
                }
            }
        }
    });
    """

    updated_html = update_html_template(str(soup), generated_js_code)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    data = generate_json_data(soup, text_tags)
    json_data_str = json.dumps(data)
    upload_json(json_data_str)

    print(f"Updated HTML with IDs written to {output_html_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py path/to/index.html")
        sys.exit(1)
    
    input_html_path = sys.argv[1]
    process_html_file(input_html_path)
