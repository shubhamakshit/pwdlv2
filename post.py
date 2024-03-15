import re,sys,os

def extract_last_segment_number(m3u8_content):
    return m3u8_content.split('\n')[m3u8_content.split('\n').index('#EXT-X-ENDLIST')-1].split('.')[0]

def replace_api_penpencil_url(m3u8_content):

        #if glv.vout: glv.dprint(f"LOCATION : {(os.getcwd()).replace('\','/')}\n") #DEUBG
        #
        # sys.stderr.write(f"AT replace_api_penpencil_url():\n content: {m3u8_content}") #debug
        #
        
        input_string = m3u8_content # Your input string

        #------------------------------------------------------------------------------------------
        # Define the regex pattern
        regex_pattern = r'https:\/\/api\.penpencil\.(co|xyz)\/v1\/videos\/get-hls-key\?videoKey[A-Za-z0-9&=.-]*'
        


        # Find the match using re.search
        match = re.search(regex_pattern, input_string)
        
        #------------------------------------------------------------------------------------------


        #------------------------------------------------------------------------------------------
        # Check if a match is found
        if match:
            # Store the matched string in a variable
            url_original = match.group(0)

            # Replace the matched string with 'enc.key'
            m3u8_content = re.sub(regex_pattern, 'enc.key', input_string)
        #------------------------------------------------------------------------------------------
        else:
            sys.stderr.write("NO MATCH FOUND AT replace_api_penpencil_url()") #debug

        #return modified m3u8 content
        return [m3u8_content, url_original]

def post_op():
     with open('main.m3u8','r') as mfile:
        m3u8_content = mfile.read()
        #print(m3u8_content) # DEBUG

        last_segment_number = extract_last_segment_number(m3u8_content)

        # replace_api_penpencil_url() returns a list with
        #   [0] = m3u8 content
        #   [1] = enc.key url
        # storing enc.key url for future use

        changed_m3u8_data = replace_api_penpencil_url(m3u8_content)

        m3u8_content = changed_m3u8_data[0]
        enc_url = changed_m3u8_data[1]

        with open('main.m3u8','w+') as m3u8_file:
            m3u8_file.write(m3u8_content)

        # downloading enc.key
        #shell(f'aria2c {enc_url} ') #legacy method
        print(enc_url)
        os.system(f'aria2c "{enc_url}"')
    
