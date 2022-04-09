
# // const canvas_width = 500;
# // const canvas_height = 500;
# // const unit_length = 8;

# // function Compute(a, b, r){
# //     var origin=[canvas_width/2, canvas_height/2];
# //     var output=[origin[0]+a*unit_length, origin[1]+b*unit_length];
# //     return output;
# // }

# // var variables = document.querySelector("#graph_parameters");
# // var canvas = document.querySelector("#myCanvas");
# // var ctx = canvas.getContext("2d");

# // for(i=0; i<=canvas_width; i+=unit_length)
# // {
# //     ctx.beginPath();
# //     ctx.moveTo(canvas_height/2, canvas_width/2-1);
# //     ctx.lineTo(canvas_height/2, canvas_width/2+1);
# //     ctx.stroke();
# // }

# // a1 = {{graph_parameters[0]}};
# // a2 = {{graph_parameters[1]}};
# // b1 = {{graph_parameters[2]}};
# // b2 = {{graph_parameters[3]}};
# // r = {{graph_parameters[4]}};

# // console.log([a1, a2, b1, b2, r]);

# // var x1=Compute(a1,b1,r)[0];
# // var y1=Compute(a1,b1,r)[1];
# // var x2=Compute(a2,b2,r)[0];
# // var y2=Compute(a2,b2,r)[1];

# // ctx.fillStyle = "black";
# // //y-axis
# // ctx.beginPath();
# // ctx.moveTo(canvas_width/2, 0);
# // ctx.lineTo(canvas_width/2, canvas_height);
# // ctx.stroke();
# // //x-axis
# // ctx.beginPath();
# // ctx.moveTo(0, canvas_height/2);
# // ctx.lineTo(canvas_width, canvas_height/2);
# // ctx.stroke();

# // ctx.beginPath();
# // ctx.arc(x1, y1, r, 0, 2*Math.PI);
# // ctx.stroke();
# // ctx.beginPath();
# // ctx.arc(x2, y2, r, 0, 2*Math.PI);
# // ctx.stroke();