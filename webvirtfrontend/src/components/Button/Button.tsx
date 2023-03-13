import { forwardRef, ReactNode } from 'react';
import tw from 'twin.macro';

interface Props {
  type?: 'submit' | 'button';
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'secondary' | 'danger';
  loading?: boolean;
  disabled?: boolean;
  children: ReactNode;
  fullWidth?: boolean;
  startIcon?: ReactNode;
  endIcon?: ReactNode;
  onlyIcon?: boolean;
}

const getBaseStyle = () =>
  tw`inline-flex items-center justify-center gap-1 font-bold transition-colors rounded-md text-body`;

const getVarianStyle = ({ variant }: { variant: Props['variant'] }) => {
  switch (variant) {
    case 'secondary': {
      return tw`border border-button-secondary bg-button-secondary hover:bg-button-secondary-hover active:border-button-secondary-active`;
    }
    case 'danger': {
      return tw`border text-button-danger border-button-danger bg-button-danger hover:bg-button-danger-hover active:border-button-danger-active`;
    }
    default: {
      return tw`text-button-default bg-button-default active:bg-button-default-active hover:bg-button-default-hover`;
    }
  }
};

const getSizeStyle = ({
  size,
  onlyIcon,
}: {
  size: Props['size'];
  onlyIcon: Props['onlyIcon'];
}) => {
  switch (size) {
    case 'sm': {
      return onlyIcon ? tw`w-8 h-8` : tw`h-8 text-xs`;
    }
    case 'md': {
      return onlyIcon ? tw`w-9 h-9` : tw`text-sm h-9`;
    }
    case 'lg': {
      return onlyIcon ? tw`w-10 h-10` : tw`h-10 text-sm`;
    }
    default: {
      return onlyIcon ? tw`w-8 h-8` : tw`h-8 text-sm`;
    }
  }
};

const getDisabledStyle = () =>
  tw`cursor-not-allowed text-button-disabled bg-button-disabled`;

export const Button = forwardRef<HTMLButtonElement, Props>(
  (
    {
      variant = 'default',
      children,
      type = 'button',
      size = 'sm',
      loading,
      fullWidth,
      disabled,
      startIcon,
      endIcon,
      onlyIcon,
      ...rest
    },
    ref,
  ): JSX.Element => {
    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || loading}
        css={[
          getBaseStyle(),
          !onlyIcon && tw`px-4`,
          getSizeStyle({ size, onlyIcon }),
          disabled || loading ? getDisabledStyle() : getVarianStyle({ variant }),
          fullWidth ? tw`w-full` : ``,
        ]}
        {...rest}
      >
        {startIcon}
        {loading ? <span>Loading...</span> : children}
        {endIcon}
      </button>
    );
  },
);

Button.displayName = 'Button';
