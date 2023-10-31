import React from 'react';
import loading_animation from '../../assets/loading_animation.svg';

const blob = new Blob([loading_animation], { type: 'image/svg+xml' });
const url = URL.createObjectURL(blob);

export const LoadingAnimation = ({ style }: { style: React.CSSProperties }) => (
  <img src={url} style={style} />
);
