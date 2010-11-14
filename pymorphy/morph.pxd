import cython

@cython.locals(l=int, vars=list, i=int)
cpdef list _get_split_variants(unicode word)

@cython.locals(item=unicode)
cpdef int _array_match(list arr, list filter)


cdef class GramForm(object):
    cpdef set form
    cpdef set denied_form

    cpdef GramForm update(self, unicode form_string)
    cpdef unicode get_form_string(self)
    cpdef int match(self, unicode gram_form)


cdef class Morph(object):
    cpdef object data
    cpdef int check_prefixes
    cpdef int predict_by_prefix
    cpdef int predict_by_suffix
    cpdef int prediction_max_prefix_len
    cpdef int prediction_min_suffix_len
    cpdef int handle_EE

    @cython.locals(paradigm=list, gram=list)
    cpdef list _get_lemma_graminfo(self, unicode lemma, unicode suffix, unicode require_prefix, unicode method_format_str)

