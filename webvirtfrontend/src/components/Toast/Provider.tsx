import { createContext, useCallback, useEffect, useState } from 'react';
import tw from 'twin.macro';

import { Toast as ToastComponent } from './Toast';

export type Toast = {
  id: number;
  type: 'success' | 'warning' | 'error';
  message: string;
};

export type ToastPayload = Omit<Toast, 'id'>;

const ToastContext = createContext<(toast: ToastPayload) => void>(() => {});

export const ToastContextProvider = ({ children }): JSX.Element => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    if (toasts.length > 0) {
      const timer = setTimeout(() => {
        setToasts(() => toasts.slice(1));
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [toasts]);

  const createToast = useCallback(
    (toast: ToastPayload) =>
      setToasts((toasts) => [...toasts, { ...toast, id: toasts.length + 1 }]),
    [toasts],
  );
  return (
    <ToastContext.Provider value={createToast}>
      <div css={tw`fixed top-0 right-0 z-20 p-4 space-y-2`}>
        {toasts.map((toast) => (
          <ToastComponent toast={toast} key={toast.id} />
        ))}
      </div>
      {children}
    </ToastContext.Provider>
  );
};

export default ToastContext;
