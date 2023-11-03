# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the hdl_registers project, a HDL register generator fast enough to run
# in real time.
# https://hdl-registers.com
# https://gitlab.com/hdl_registers/hdl_registers
# --------------------------------------------------------------------------------------------------

# Standard libraries
from abc import ABC, abstractmethod

# Local folder libraries
from .register_field_type import FieldType, Unsigned

DEFAULT_FIELD_TYPE = Unsigned()


class RegisterField(ABC):

    """
    Meta class for all register fields (bits, bit vectors, integers, ...).
    Lists a few methods that must be implemented.
    """

    @property
    def max_binary_value(self) -> int:
        """
        Get the maximum value, represented as a positive integer, that this
        field can hold given its width.
        """
        return 2**self.width - 1

    @property
    def range_str(self) -> str:
        """
        Return the bits that this field occupies in a readable format.
        The way it shall appear in documentation.
        """
        if self.width == 1:
            return f"{self.base_index}"

        return f"{self.base_index + self.width - 1}:{self.base_index}"

    @property
    def field_type(self) -> FieldType:
        """
        The field type (Unsigned, Signed, UnsignedFixedPoint, SignedFixedPoint, ...)
        used to interpret the bits of the field.
        """
        # Default for all RegisterFields
        return DEFAULT_FIELD_TYPE

    @property
    @abstractmethod
    def width(self) -> int:
        """
        Return the width, in number of bits, that this field occupies.
        """
        raise NotImplementedError("Must be implemented in child class")

    @property
    @abstractmethod
    def base_index(self) -> int:
        """
        The index within the register for the lowest bit of this field.
        """
        raise NotImplementedError("Must be implemented in child class")

    @property
    @abstractmethod
    def default_value_str(self) -> str:
        """
        Return a formatted string of the default value. The way it shall appear
        in documentation.
        """
        raise NotImplementedError("Must be implemented in child class")

    @property
    @abstractmethod
    def default_value_uint(self) -> int:
        """
        Return a the default value as an unsigned int.
        """
        raise NotImplementedError("Must be implemented in child class")

    def get_value(self, register_value: int) -> float:
        """
        Get the value of this field, given the supplied register value.
        Child classes might implement sanity checks on the value.

        Arguments:
            register_value: Value of the register that this field belongs to.

        Returns:
            The value of the field.
        """
        shift = self.base_index

        mask_at_base = (1 << self.width) - 1
        mask = mask_at_base << shift

        value_unsigned = (register_value & mask) >> shift
        field_value = self.field_type.convert_from_unsigned_binary(self.width, value_unsigned)

        return field_value

    def set_value(self, field_value: float) -> int:
        """
        Convert the supplied value into the bit-shifted unsigned integer ready
        to be written to the register. The bits of the other fields in the
        register are masked out and will be set to zero.

        Arguments:
            field_value: Desired value to set the field to.

        Returns:
            The register value
        """
        value_unsigned = self.field_type.convert_to_unsigned_binary(self.width, field_value)
        max_value = self.max_binary_value
        if not 0 <= value_unsigned <= max_value:
            raise ValueError(
                f"Value: {value_unsigned} is invalid for unsigned of width {self.width}"
            )

        mask = max_value << self.base_index
        value_shifted = value_unsigned << self.base_index

        return value_shifted & mask
