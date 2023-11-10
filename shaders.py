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
out float time2;

void main(){
    newPos = vec4(position.x, position.y, position.z, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs= texCoords;
    outNormals= (modelMatrix * vec4(normals, 0.0)).xyz;
    time2 = time;
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

    vec3 baseColor= vec3(0.7529, 0.5725, 0.3765);
    vec3 lineColor= vec3(0.808, 0.110, 0.341);

    vec3 color = mix(baseColor, lineColor, pulse(UVs.y, 10.0) * wave);

    float diffuse = 0.5 + dot(outNormals, dir);
    fragColor = vec4(diffuse * color, 1.0);
}
'''

siren_shader= ''' 
#version 450 core

in float time2;
in vec3 outNormals;

void main(){
    float theta = time2 * 2.0;

    vec3 dir = vec3(cos(theta), 0, sin(theta));
    vec3 dir2= vec3(sin(theta), 0, cos(theta));

    float diffuse = pow(dot(outNormals, dir), 2.0);
    float diffuse2= pow(dot(outNormals, dir2), 2.0);

    //Colores con entre los que cambia
    vec3 col1 = diffuse * vec3(0, 1, 0);
    vec3 col2 = diffuse2 * vec3(0, 0, 1);

    gl_FragColor = vec4(col1 + col2, 1.0);
}
'''

glitch_shader= ''' 
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 UVs;
in float time2;
out vec4 fragColor;

void main(){
    float glitch = smoothstep(0.9, 1.0, sin(time2 * 10.0));
    vec3 color = vec3(glitch * texture(tex, UVs).rgb);

    fragColor= vec4(color, 1.0);
}
'''

mixColors_shader= ''' 
#version 450 core

in vec2 UVs;
out vec4 fragColor;

void main() {
    // Colores iniciales
    vec3 color1 = vec3(1.0, 0.0, 0.0);
    vec3 color2 = vec3(0.0, 0.0, 1.0);

    // Interpolación lineal entre los dos colores basada en la coordenada y
    vec3 finalColor = mix(color1, color2, UVs.y);

    fragColor = vec4(finalColor, 1.0);
}
'''