import React, { forwardRef } from 'react';
import tw from 'twin.macro';

interface Props {
  id: string;
  name: string;
  type?: 'text' | 'number' | 'email' | 'password';
  placeholder: string;
  label?: string;
  hint?: string;
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  required?: boolean;
  readonly?: boolean;
  error?: boolean | string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const getBaseStyle = () =>
  tw`w-full px-4 text-sm transition-colors border rounded-md bg-input-default`;

const getDisabledStyle = () => tw`bg-input-disabled`;

const getBaseFocusStyle = () =>
  tw`border-input-default focus:border-blue-700 focus:ring-1 focus:ring-blue-700`;

const getErrorFocusStyle = () =>
  tw`border-red-500 focus:border-red-500 focus:ring-1 focus:ring-red-500`;

const getSizeStyle = ({ size }: { size: Props['size'] }) => {
  switch (size) {
    case 'sm': {
      return tw`h-8 text-xs`;
    }
    case 'md': {
      return tw`text-sm h-9`;
    }
    case 'lg': {
      return tw`h-10 text-sm`;
    }
    default: {
      return tw`h-8 text-sm`;
    }
  }
};

const Input = forwardRef<HTMLInputElement, Props>(
  (
    {
      id,
      name,
      label,
      hint,
      type = 'text',
      size = 'md',
      required,
      readonly = false,
      disabled,
      error,
      ...rest
    },
    ref,
  ): JSX.Element => {
    return (
      <div>
        <label htmlFor={id} css={tw`inline-block mb-1 text-xs font-bold`}>
          {label && <span>{label}</span>}
          {required && <span css={tw`text-red-500`}>*</span>}
        </label>

        <input
          id={id}
          name={name}
          ref={ref}
          type={type}
          disabled={disabled}
          readOnly={readonly}
          css={[
            getBaseStyle(),
            (disabled || readonly) && getDisabledStyle(),
            getSizeStyle({ size }),
            error ? getErrorFocusStyle() : getBaseFocusStyle(),
          ]}
          {...rest}
        />

        {hint || error ? (
          <p css={[tw`mt-1 text-xs`, error ? tw`text-red-500` : tw`text-alt2`]}>
            {typeof error === 'string' && error !== '' ? error : hint}
          </p>
        ) : null}
      </div>
    );
  },
);

Input.displayName = 'Input';

export default Input;
