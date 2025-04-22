// components/DraggableText.js
import React from "react";
import { Text } from "react-konva";

export default function DraggableText({ slug, text, initial, fontSize, onChange }) {

  return (
    <Text
      text={text}
      x={initial.x}
      y={initial.y}
      fontSize={fontSize}
      fontFamily="Fredoka"
      draggable
      onDragEnd={(e) => {
        onChange?.(slug, e.target.x(), e.target.y());
      }}
      shadowColor="black"
      fill="#441305"
      shadowBlur={1}
    />
  );
}
