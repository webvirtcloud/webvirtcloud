import { useContext } from 'react';

import ToastContext from './Provider';

export default function useToastContext() {
  return useContext(ToastContext);
}
