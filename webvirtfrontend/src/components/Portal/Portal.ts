import { ReactNode, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

type Props = {
  children: ReactNode;
};

export const Portal = ({ children }: Props) => {
  const rootRef = useRef<HTMLDivElement>();
  const [mounted, setMounted] = useState(false);

  useLayoutEffect(() => {
    rootRef.current = document.createElement('div');
    rootRef.current.setAttribute('data-react-portal', 'true');
    document.body.appendChild(rootRef.current);

    setMounted(true);

    return () => {
      rootRef.current?.remove();
    };
  }, []);

  if (!mounted || !rootRef.current) {
    return null;
  }

  return createPortal(children, rootRef.current);
};
