
service StableDiffusion {
    void generate(1:string outputPath, 2:string textInput = "", 3:string imagePath = "", 4:i16 width = 512, 5:i16 height = 512, 6:i16 steps = 50, 7: optional i64 seed),
}