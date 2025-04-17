from pathlib import Path
import xml.etree.ElementTree as ET


def create_drawing_XML(
    tokens: list[str], 
    orientations: list[int], 
    view_box_val: int = 500, 
    scale: float = 0.65, 
    stroke_width: int = 5,
    path_to_ripple_images: Path = Path(f'src/ripples/images')
) -> ET.Element:
    element_to_return: ET.ElementTree = ET.ElementTree(
        ET.fromstring(
            f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{view_box_val}" height="{view_box_val}">
            </svg>
            '''
        )
    )
    element_to_return_root: ET.Element = element_to_return.getroot()
    
    num_tokens: int = len(tokens)
    for i, token in enumerate(tokens):
        tokenElement: ET.Element = ET.parse(str(path_to_ripple_images / Path(f"{token}.svg"))).getroot()
        scale_value = scale ** (num_tokens - (i + 1))
        tokenElement.tag = 'g'
        tokenElement.attrib = {
            'id': f'{token}_{i}',
            'xmlns': 'http://www.w3.org/2000/svg',
            'transform-origin': f'{view_box_val//2} {view_box_val//2}',
            'transform': f'scale({scale_value}) rotate({90 * orientations[i]})',
        }
        
        _enforce_non_scaling_stroke_and_stroke_width_on_path_elements(tokenElement, stroke_width)
        
        
        element_to_return_root.append(tokenElement)
    

    return element_to_return

def _enforce_non_scaling_stroke_and_stroke_width_on_path_elements(element: ET.Element, stroke_width: int):
    for child in element:
        if child.tag == 'path':
            child.attrib = child.attrib | {
                    'vector-effect': 'non-scaling-stroke',  # Important to enforce
                    'stroke-width': str(stroke_width)
                }
        _enforce_non_scaling_stroke_and_stroke_width_on_path_elements(child, stroke_width)


if __name__ == "__main__":
    create_drawing_XML(['ae', 's', 'ii', 'vh'], [0, 1, 2, 3]).write("output1.svg")
