xof 0303txt 0032

Frame Root {
  FrameTransformMatrix {
     1.000000, 0.000000, 0.000000, 0.000000,
     0.000000,-0.000000, 1.000000, 0.000000,
     0.000000, 1.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 1.000000;;
  }
  Frame Plane {
    FrameTransformMatrix {
       1.000000, 0.000000, 0.000000, 0.000000,
       0.000000, 1.000000, 0.000000, 0.000000,
       0.000000, 0.000000, 1.000000, 0.000000,
       0.000000, 0.000000, 0.000000, 1.000000;;
    }
    Mesh { // Plane mesh
      4;
       1.000000;-1.000000; 0.000000;,
      -1.000000;-1.000000; 0.000000;,
       1.000000; 1.000000; 0.000000;,
      -1.000000; 1.000000; 0.000000;;
      1;
      4;3,2,0,1,;
      MeshNormals { // Plane normals
        1;
         0.000000; 0.000000; 1.000000;;
        1;
        4;0,0,0,0,;
      } // End of Plane normals
      MeshMaterialList { // Plane material list
        1;
        1;
        0;;
        Material Material_001 {
           0.640000; 0.640000; 0.640000; 1.000000;;
           96.078431;
           0.500000; 0.500000; 0.500000;;
           0.000000; 0.000000; 0.000000;;
          TextureFilename {"../../Texture/box_t.png";}
        }
      } // End of Plane material list
    } // End of Plane mesh
  } // End of Plane
} // End of Root
