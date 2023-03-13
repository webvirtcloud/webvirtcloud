import 'twin.macro';

import { DOMAttributes } from 'react';
import styledImport, { css as cssImport, CSSProp } from 'styled-components';

declare module 'twin.macro' {
  // The styled and css imports
  const styled: typeof styledImport;
  const css: typeof cssImport;
}

declare module 'react' {
  // The tw and css prop
  interface DOMAttributes<T> {
    tw?: string;
    css?: CSSInterpolation;
  }
}

// The 'as' prop on styled components
declare global {
  namespace JSX {
    interface IntrinsicAttributes<T> extends DOMAttributes<T> {
      as?: string | Element;
    }
  }
}
