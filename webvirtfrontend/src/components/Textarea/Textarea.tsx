import React, { forwardRef, TextareaHTMLAttributes } from 'react';
import tw from 'twin.macro';

interface Props extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  id: string;
  name: string;
  placeholder: string;
  label: string;
  rows?: number;
  hint?: string;
  size?: 'sm' | 'md';
  error?: boolean | string;
  disabled?: boolean;
  required?: boolean;
  readonly?: boolean;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onBlur: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
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
      return tw`text-xs`;
    }
    case 'md': {
      return tw`text-sm`;
    }
    default: {
      return tw`text-sm`;
    }
  }
};

const Textarea = forwardRef<HTMLTextAreaElement, Props>(
  (
    {
      id,
      name,
      label,
      disabled,
      error,
      readonly = false,
      size = 'md',
      required,
      rows = 5,
      hint,
      ...rest
    },
    ref,
  ): JSX.Element => {
    return (
      <div css={tw`flex flex-col`}>
        <label htmlFor={id} css={tw`inline-block mb-1 text-xs font-bold`}>
          {label}
          {required && <span css={tw`text-red-500`}>*</span>}
        </label>

        <textarea
          id={id}
          name={name}
          ref={ref}
          rows={rows}
          readOnly={readonly}
          disabled={disabled}
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

Textarea.displayName = 'Textarea';

export default Textarea;
