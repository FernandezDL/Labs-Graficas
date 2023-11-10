vertex_shader = '''
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;
out vec4 newPos;

void main(){
    newPos = vec4(position.x, position.y, position.z, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs= texCoords;
    outNormals= (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

fragment_shader = ''' 
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;
out vec4 fragColor;

void main(){
    fragColor= texture(tex, UVs) ;
}
'''

pie_shader = '''
#version 450 core

in vec2 UVs;
in vec3 outNormals;
in vec4 newPos;
out vec4 fragColor;

float pulse(float val, float dst){
    return floor(mod(val * dst, 1.0) + 0.5);
}

void main(){
    vec3 dir = vec3(0, 1, 0);
    
    float wave = 0.5 + 0.5 * sin(newPos.x * 5.0);
    vec3 color = vec3(1, pulse(UVs.y, 10.0) * wave, 1);

    float diffuse = 0.5 + dot(outNormals, dir);
    fragColor = vec4(diffuse * color, 1.0);
}
'''