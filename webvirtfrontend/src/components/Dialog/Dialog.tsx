import { AnimatePresence, motion } from 'framer-motion';
import { ReactNode } from 'react';
import tw from 'twin.macro';

import { Portal } from '../Portal';
import { DialogHeader } from './DialogHeader';

type Props = {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: ReactNode;
};

const DialogMask = motion(tw.div`
  fixed
  z-40
  inset-0
  bg-black/50
  flex
  items-center
  justify-center
  backdrop-blur-sm
`);

const DialogContainer = motion(tw.div`
  bg-base
  w-full
  max-w-lg
  p-4
  rounded-md
  focus:outline
  focus:outline-2
  focus:outline-offset-2
  focus:outline-blue-700
`);

export default function Dialog({ isOpen, title, onClose, children }: Props) {
  return (
    <Portal>
      <AnimatePresence>
        {isOpen && (
          <DialogMask
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <DialogContainer
              initial={{ opacity: 0, scale: 1.1 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.1 }}
              transition={{ type: 'spring' }}
              tabIndex={0}
            >
              <DialogHeader onClose={onClose} title={title} />
              <div>{children}</div>
            </DialogContainer>
          </DialogMask>
        )}
      </AnimatePresence>
    </Portal>
  );
}
